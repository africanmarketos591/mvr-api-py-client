import time
from typing import Optional, Dict, Any

import requests

from .models import (
    AMOSConfig,
    AMOSScoreRequest,
    AMOSScoreResponse,
    HealthResponse,
    AMOSErrorResponse,
)


class AMOSApiError(Exception):
    """
    Base exception for AMOS-MVR API errors.

    Wraps the server-side AMOSErrorResponse payload so callers can inspect:
      - error_data.error
      - error_data.details
      - error_data.request_id
    """

    def __init__(self, error_data: AMOSErrorResponse):
        self.error_data = error_data
        # Best-effort human-readable message
        msg = getattr(error_data, "error", None) or "AMOS API error"
        super().__init__(msg)


class AMOSClient:
    """
    Main AMOS-MVR API client using License + Buyer Email authentication.

    Required headers (automatically set):
      - x-mvr-license
      - x-buyer-email

    Endpoints implemented:
      - POST /v1/amos/score  -> score_amos(...)
      - GET  /health         -> get_health()
    """

    def __init__(self, config: AMOSConfig):
        self.config = config

        # Persistent HTTP session
        self.session = requests.Session()
        self.session.headers.update(
            {
                "x-mvr-license": config.license_key,
                "x-buyer-email": config.buyer_email,
                "Content-Type": "application/json",
                "User-Agent": "amos-mvr-api-py-client/1.0.0",
            }
        )

        self.base_url: str = config.base_url
        self.max_retries: int = config.max_retries
        self.timeout: float = config.timeout

    # ------------------------------------------------------------------
    # INTERNAL REQUEST WRAPPER
    # ------------------------------------------------------------------
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Low-level HTTP request with retry + basic rate-limit handling.

        Returns:
            Parsed JSON body (dict) on HTTP 200.

        Raises:
            AMOSApiError for non-200 responses or terminal network failures.
        """

        url = f"{self.base_url}{endpoint}"

        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method,
                    url,
                    timeout=self.timeout,
                    **kwargs,
                )

                # Try to parse JSON; if this fails we still want some context
                try:
                    data = response.json()
                except ValueError:
                    data = {
                        "error": f"Non-JSON response from AMOS API (status {response.status_code})",
                        "details": {"text": response.text},
                        "request_id": None,
                    }

                # -------------------------
                # Successful Response
                # -------------------------
                if response.status_code == 200:
                    if isinstance(data, dict):
                        return data
                    # Defensive: some servers may return a list; wrap it
                    return {"data": data}

                # -------------------------
                # Rate Limited (429)
                # -------------------------
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    if attempt < self.max_retries:
                        time.sleep(retry_after)
                        continue

                # -------------------------
                # Other API Errors
                # -------------------------
                # Best-effort to map server JSON into AMOSErrorResponse
                if isinstance(data, dict):
                    try:
                        error_obj = AMOSErrorResponse(**data)
                    except TypeError:
                        # Fallback if shape does not strictly match model
                        error_obj = AMOSErrorResponse(
                            error=str(data.get("error", "Unknown AMOS API error")),
                            details=data.get("details"),
                            request_id=data.get("request_id"),
                        )
                else:
                    error_obj = AMOSErrorResponse(
                        error="Unknown AMOS API error",
                        details={"raw": data},
                        request_id=None,
                    )

                raise AMOSApiError(error_obj)

            except requests.exceptions.RequestException as e:
                # Network errors (timeouts, connection drops)
                if attempt == self.max_retries:
                    error_obj = AMOSErrorResponse(
                        error="NETWORK_ERROR",
                        details={"exception": str(e)},
                        request_id=None,
                    )
                    raise AMOSApiError(error_obj)

                # Simple exponential backoff
                time.sleep(2 ** attempt)

        # This should be unreachable, but keeps type-checkers happy
        error_obj = AMOSErrorResponse(
            error="UNKNOWN_ERROR",
            details={"reason": "Exhausted retries without response"},
            request_id=None,
        )
        raise AMOSApiError(error_obj)

    # ------------------------------------------------------------------
    # PUBLIC API METHODS
    # ------------------------------------------------------------------
    def score_amos(self, request: AMOSScoreRequest) -> AMOSScoreResponse:
        """
        POST /v1/amos/score

        Compute AMOS relational risk, porosity, MVR, and safe credit limits.

        Args:
            request: AMOSScoreRequest payload.

        Returns:
            AMOSScoreResponse
        """
        payload = request.dict() if hasattr(request, "dict") else request.__dict__
        data = self._request("POST", "/v1/amos/score", json=payload)
        return AMOSScoreResponse(**data)

    def get_health(self) -> HealthResponse:
        """
        GET /health

        Lightweight health probe. Returns engine version, wrapper, and timestamp.

        Returns:
            HealthResponse
        """
        data = self._request("GET", "/health")
        return HealthResponse(**data)
