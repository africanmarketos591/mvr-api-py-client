from __future__ import annotations

import time
from typing import Any, Dict, Optional

import requests

from .models import MVRConfig


class MVRApiError(Exception):
    """Structured exception for MVR API transport and validation failures."""

    def __init__(self, message: str, status_code: Optional[int] = None, error_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_data = error_data or {}


class MVRClient:
    """Small Python client for the current MVR API v6.32.x public surface."""

    def __init__(self, config: Optional[MVRConfig] = None, **kwargs: Any):
        self.config = config or MVRConfig(**kwargs)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "X-API-Key": self.config.api_key,
                "X-Response-Profile": self.config.response_profile,
                "User-Agent": "mvr-api-py-client/6.32.1",
            }
        )

    def _request(self, method: str, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.config.base_url.rstrip('/')}{endpoint}"

        for attempt in range(self.config.max_retries + 1):
            try:
                response = self.session.request(
                    method,
                    url,
                    json=payload if method.upper() != "GET" else None,
                    timeout=self.config.timeout,
                )
                try:
                    data = response.json()
                except ValueError:
                    data = {"error": "NON_JSON_RESPONSE", "message": response.text}

                if 200 <= response.status_code < 300:
                    return data if isinstance(data, dict) else {"data": data}

                if response.status_code == 429 and attempt < self.config.max_retries:
                    retry_after = int(response.headers.get("Retry-After", "2"))
                    time.sleep(retry_after)
                    continue

                message = data.get("message") or data.get("error") or f"MVR API HTTP {response.status_code}"
                raise MVRApiError(message, response.status_code, data)

            except requests.RequestException as exc:
                if attempt == self.config.max_retries:
                    raise MVRApiError(str(exc), error_data={"error": "NETWORK_ERROR", "message": str(exc)}) from exc
                time.sleep(2**attempt)

        raise MVRApiError("MVR API request failed", error_data={"error": "UNKNOWN_ERROR"})

    def auth_check(self) -> Dict[str, Any]:
        return self._request("POST", "/v1/auth-check", {})

    def entity_resolve(self, entity_name: str, country: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"entity_name": entity_name, **extra}
        if country:
            payload["country"] = country
        return self._request("POST", "/v1/entity-resolve", payload)

    def evidence_completeness(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/v1/evidence-completeness", payload)

    def context_compile(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/v1/context/compile", payload)

    def decision_check(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/v1/decision-check", payload)

    def model_card(self) -> Dict[str, Any]:
        return self._request("GET", "/v1/model-card")

    def capabilities(self) -> Dict[str, Any]:
        return self._request("GET", "/v1/capabilities")

    def health(self) -> Dict[str, Any]:
        return self._request("GET", "/health")


MVRApiClient = MVRClient

