from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ============================================================
# CONFIG
# ============================================================

class AMOSConfig(BaseModel):
    """
    Configuration for the AMOS-MVR API client.
    """
    license_key: str = Field(..., description="MVR / AMOS license key (x-mvr-license).")
    buyer_email: str = Field(..., description="Buyer email associated with the license (x-buyer-email).")
    base_url: str = Field(
        default="https://africanmarketos.com",
        description="Base URL for the AMOS-MVR API.",
    )
    timeout: float = Field(default=30.0, description="Request timeout in seconds.")
    max_retries: int = Field(default=3, description="Maximum number of retries for transient errors.")


# ============================================================
# REQUEST MODELS
# ============================================================

class SectorEnum(str, Enum):
    GENERIC = "GENERIC"
    FINTECH = "FINTECH"
    FMCG_RETAIL = "FMCG_RETAIL"
    FMCG_BEVERAGE = "FMCG_BEVERAGE"
    FMCG_OILS = "FMCG_OILS"
    FMCG_DAIRY = "FMCG_DAIRY"
    FMCG_PERSONAL_CARE = "FMCG_PERSONAL_CARE"
    FMCG_FOODS = "FMCG_FOODS"
    FMCG_ALCOHOL = "FMCG_ALCOHOL"


class MVRBlock(BaseModel):
    """
    Explicit Minimum Viable Relationships (MVR) scores.

    If omitted in the request, AMOS infers MVR-I and dimensions from financial/activity signals.
    """
    mvr_i: Optional[float] = Field(
        None, ge=0, le=100,
        description="Minimum Viable Relationships Index (0–100)."
    )
    embeddedness: Optional[float] = Field(None, ge=0, le=100)
    trust: Optional[float] = Field(None, ge=0, le=100)
    cultural_fit: Optional[float] = Field(None, ge=0, le=100)
    reciprocity: Optional[float] = Field(None, ge=0, le=100)
    guardian_vouchers: Optional[float] = Field(None, ge=0, le=100)
    continuity: Optional[float] = Field(None, ge=0, le=100)
    channel_permission: Optional[float] = Field(None, ge=0, le=100)


class AMOSScoreRequest(BaseModel):
    """
    AMOS score request – maps closely to the OpenAPI AMOSScoreRequest schema.
    """

    # Required core identifiers
    amos_id: str = Field(..., description="Stable identifier for this entity within your systems.")
    sector: SectorEnum = Field(..., description="Sector tag used to select physics and rhythms.")
    region: str = Field(..., description="Region code used for seasonal pressure (EA, WA, ZA, GENERIC, etc.).")

    # Required core financials & activity
    revenue: float = Field(..., ge=0, description="Annual revenue in local currency.")
    cash: float = Field(..., ge=0, description="Cash and cash-equivalents in local currency.")
    days_silent: float = Field(..., ge=0, description="Days since last observed activity.")
    occupancy_rate: float = Field(
        ...,
        ge=0,
        le=100,
        description="Utilization / occupancy as a percentage (0–100).",
    )
    collection_rate: float = Field(
        ...,
        ge=0,
        le=100,
        description="Collection rate as a percentage (0–100).",
    )

    # Optional identifiers / aliases
    id: Optional[str] = Field(None, description="Optional legacy ID (alias for amos_id).")
    name: Optional[str] = Field(None, description="Human-readable name of the entity.")
    legal_name: Optional[str] = Field(None, description="Legal registered name (if different from name).")

    # Optional financials & operational metrics
    total_revenue: Optional[float] = Field(None, ge=0, description="Optional alias for revenue.")
    expenses: Optional[float] = Field(None, ge=0, description="Operating expenses / COGS.")
    opex: Optional[float] = Field(None, ge=0, description="Optional alias for expenses.")
    cash_balance: Optional[float] = Field(None, ge=0, description="Optional alias for cash.")
    total_debt: Optional[float] = Field(None, ge=0, description="Total interest-bearing debt.")
    debt_total: Optional[float] = Field(None, ge=0, description="Optional alias for total_debt.")
    arrears: Optional[float] = Field(None, ge=0, description="Overdue receivables / arrears.")
    overdue: Optional[float] = Field(None, ge=0, description="Optional alias for arrears.")
    revenue_growth: Optional[float] = Field(None, description="Annual revenue growth rate (e.g., 0.10 for +10% YoY).")

    days_since_last_activity: Optional[float] = Field(None, ge=0)
    days_since_last_scan: Optional[float] = Field(None, ge=0)

    guardian_endorsements: Optional[float] = Field(
        None, ge=0,
        description="Number of credible guardians / endorsers willing to vouch."
    )
    number_of_customers: Optional[float] = Field(None, ge=0)
    number_of_suppliers: Optional[float] = Field(None, ge=0)

    grant_dependency: Optional[float] = Field(
        None, ge=0, le=1,
        description="Fraction of revenue that is grant/donor funded (0–1)."
    )

    active_users: Optional[float] = Field(None, ge=0)
    active_customers: Optional[float] = Field(None, ge=0, description="Optional alias for active_users.")

    sku_sales_8w: Optional[List[float]] = Field(
        None, description="Optional SKU-level sales volumes for up to 8 weeks."
    )
    promo_units: Optional[float] = Field(None, ge=0)
    baseline_units: Optional[float] = Field(None, ge=0)

    # FX & currency
    currency: Optional[str] = Field(None, description="ISO or local currency code (e.g. KES, ZAR, GHS, EUR).")
    fx_rate: Optional[float] = Field(None, ge=0)
    fx_rate_12m_ago: Optional[float] = Field(None, ge=0)
    forward_cover: Optional[float] = Field(None, ge=0)
    fx_exposed_debt: Optional[float] = Field(None, ge=0)

    # Infrastructure & corridor
    outage_hours_per_day: Optional[float] = Field(None, ge=0)
    diesel_share_opex: Optional[float] = Field(None, ge=0, le=1)
    corridor_id: Optional[str] = None
    port_dwell_days: Optional[float] = Field(None, ge=0)
    truck_turnaround_days: Optional[float] = Field(None, ge=0)

    # Credit configuration
    current_credit_limit_local: Optional[float] = Field(None, ge=0)
    prev_ghosting: Optional[float] = None

    # Relational / text
    mvr: Optional[MVRBlock] = None
    unstructured_text: Optional[str] = Field(
        None,
        description="Free-text description; scanned for fraud / scandal / social sanction language.",
    )


# ============================================================
# RESPONSE MODELS
# ============================================================

class ConfidenceInterval(BaseModel):
    lower: float
    upper: float
    error: float


class GhostingBlock(BaseModel):
    flag: Optional[bool] = None
    isDead: Optional[bool] = None
    impact: Optional[float] = None
    survival_probability: Optional[float] = None
    days_to_ghost: Optional[float] = None
    expectedRhythm: Optional[float] = None


class ExplanationBlock(BaseModel):
    porosity: Optional[str] = None
    mvr_shield: Optional[str] = None
    mvr_shield_factor: Optional[str] = None
    final_contained_pd: Optional[str] = None
    shield_impact_percentage: Optional[str] = None
    headline: Optional[str] = None
    risk_narrative: Optional[str] = None


class CashMetricsBlock(BaseModel):
    cash_runway_days: Optional[int] = None
    runwayState: Optional[str] = Field(
        None,
        description="One of CRITICAL, DANGER, WATCH, HEALTHY, STRONG.",
    )
    net_cash: Optional[float] = None
    burn_rate_per_day: Optional[float] = None


class DiagnosticsBlock(BaseModel):
    AFI_SCORE: Optional[float] = None
    POTEMKIN_RAW_GAP: Optional[float] = None
    POTEMKIN_GAP: Optional[float] = None
    CANNIBALISATION_RISK: Optional[float] = None
    SKU_VOLATILITY_CV: Optional[float] = None
    SKU_SAMPLE_SIZE: Optional[int] = None


class AMOSMeta(BaseModel):
    EXPLANATION: Optional[ExplanationBlock] = None

    SECTOR: Optional[str] = None
    REGION: Optional[str] = None
    GRANT_DEPENDENCY: Optional[float] = None
    DAYS_SILENT: Optional[float] = None
    PD_GHOST: Optional[float] = None

    ghosting: Optional[GhostingBlock] = None

    HAS_POTEMKIN_RISK: Optional[bool] = None
    POTEMKIN_GAP_BAND: Optional[str] = Field(
        None,
        description='One of "NONE", "LOW", "HIGH".',
    )

    MVR_I: Optional[float] = None
    MVR_BAND: Optional[str] = Field(
        None,
        description='One of "EMBEDDED", "VIABLE", "FRAGILE".',
    )
    MVR_STRONGEST_DIMENSIONS: Optional[List[str]] = None
    MVR_WEAKEST_DIMENSIONS: Optional[List[str]] = None

    MVR_RV: Optional[float] = None
    MVR_WV: Optional[float] = None
    MVR_GD: Optional[float] = None
    MVR_EQ: Optional[float] = None
    MVR_AS: Optional[float] = None
    MVR_RC: Optional[float] = None

    COLLECTION_RATE: Optional[float] = None

    FX_GAP_RATIO: Optional[float] = None
    FX_PD_MULTIPLIER: Optional[float] = None
    COLD_CHAIN_LEAKAGE: Optional[float] = None
    CORRIDOR_LEAKAGE: Optional[float] = None

    PROMO_INCREMENTALITY: Optional[float] = None
    PROMO_QUALITY: Optional[str] = None

    DAYS_TO_DEATH_CAPPED: Optional[bool] = None
    TIMELINE_SOURCE: Optional[str] = None
    TIMELINE_TREND: Optional[str] = None

    DATA_COMPLETENESS_SCORE: Optional[int] = None
    MISSING_FIELDS: Optional[List[str]] = None
    CRITICAL_MISSING_FIELDS: Optional[List[str]] = None

    MVR_GATE_DECISION: Optional[str] = None
    MVR_GATE_REASONS: Optional[List[str]] = None

    COMPASS_FIT_BAND: Optional[str] = None
    COMPASS_MVR_QUADRANT: Optional[str] = None

    HEADLINE: Optional[str] = None
    FLAGS: Optional[List[str]] = None

    NETWORK_HEALTH: Optional[float] = None

    CASH_METRICS: Optional[CashMetricsBlock] = None
    DIAGNOSTICS: Optional[DiagnosticsBlock] = None

    SEASONAL_FACTOR: Optional[float] = None
    GRANT_HAIRCUT_APPLIED: Optional[bool] = None


class CreditEngineBlock(BaseModel):
    ESTIMATED_SAFE_CREDIT_LIMIT_LOCAL: Optional[float] = None
    ESTIMATED_SAFE_CREDIT_LIMIT_USD: Optional[float] = None
    RECOMMENDED_ACTION: Optional[str] = None
    MVR_DECISION: Optional[str] = None
    SEASONAL_FACTOR: Optional[float] = None
    GRANT_HAIRCUT_APPLIED: Optional[bool] = None
    EXPOSURE_TO_REVENUE_RATIO: Optional[float] = None
    RECOMMENDED_TO_CURRENT_RATIO: Optional[float] = None


class WrapperBlock(BaseModel):
    version: Optional[str] = None
    core_version: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: Optional[datetime] = None


class ModelMetadata(BaseModel):
    model_version: Optional[str] = None
    core_version: Optional[str] = None
    wrapper_version: Optional[str] = None
    calibration_date: Optional[str] = None
    regulatory_status: Optional[str] = None
    physics_framework: Optional[str] = None


class AMOSScoreResponse(BaseModel):
    """
    Core AMOS scoring response.
    """
    RRS_SCORE: float
    RRS_CONFIDENT: float
    RRS_CONFIDENCE: int = Field(..., ge=0, le=100)
    RRS_CONFIDENCE_INTERVAL: ConfidenceInterval
    Pz_POROSITY: float = Field(..., ge=0, le=1)
    meta: AMOSMeta
    CREDIT_ENGINE: CreditEngineBlock
    WRAPPER: WrapperBlock
    MODEL_METADATA: ModelMetadata


class AMOSErrorResponse(BaseModel):
    """
    Error envelope for validation, data-quality veto, auth, or internal errors.
    """
    error: str
    details: Optional[Any] = None
    request_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    wrapper: str
    request_id: Optional[str] = None
    timestamp: datetime
