from __future__ import annotations

import os
from typing import Literal, Optional

from pydantic import BaseModel, Field


class MVRConfig(BaseModel):
    """Configuration for the MVR API client."""

    api_key: str = Field(default_factory=lambda: os.getenv("MVR_API_KEY", "mvr-demo-key-2026"))
    base_url: str = "https://africanmarketos.com"
    timeout: float = 90.0
    max_retries: int = 1
    response_profile: Literal["full_advisory", "strict_calibrated"] = "full_advisory"


class SandboxMarkers(BaseModel):
    environment: Optional[str] = None
    illustrative_only: Optional[bool] = None
    not_for_production: Optional[bool] = None
