"""African Market OS — AMOS-MVR API Python Client."""

from .client import AMOSClient, AMOSApiError
from .models import (
    AMOSConfig,
    AMOSScoreRequest,
    AMOSScoreResponse,
    HealthResponse,
    AMOSErrorResponse,
    AMOSMeta,
    CreditEngineBlock,
    WrapperBlock,
    ModelMetadata,
    ConfidenceInterval,
    GhostingBlock,
    ExplanationBlock,
    CashMetricsBlock,
    DiagnosticsBlock,
    SectorEnum,
    MVRBlock,
)

__version__ = "1.0.0"

__all__ = [
    # Client + config
    "AMOSClient",
    "AMOSApiError",
    "AMOSConfig",

    # Core request/response
    "AMOSScoreRequest",
    "AMOSScoreResponse",
    "HealthResponse",
    "AMOSErrorResponse",

    # Supporting models
    "AMOSMeta",
    "CreditEngineBlock",
    "WrapperBlock",
    "ModelMetadata",
    "ConfidenceInterval",
    "GhostingBlock",
    "ExplanationBlock",
    "CashMetricsBlock",
    "DiagnosticsBlock",
    "SectorEnum",
    "MVRBlock",
]
