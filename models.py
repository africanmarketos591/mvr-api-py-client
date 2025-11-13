from typing import List, Optional, Dict, Any
from pydantic import BaseModel


# ---------------------------
# Attribution & Version Info
# ---------------------------

class AttributionObject(BaseModel):
    framework: str
    creator: str
    source: str
    license: str
    doi: Optional[str] = None


class VersionInfo(BaseModel):
    api: str
    feature: Optional[str] = None
    method: Optional[str] = None
    model: Optional[str] = None
    mvr_proprietary: bool


# ---------------------------
#     Scores Response
# ---------------------------

class MVRDimension(BaseModel):
    name: str
    score: float
    confidence: float
    threshold_ok: bool
    binding: bool
    evidence_ptrs: List[str]


class ScoreResponse(BaseModel):
    ok: bool
    mvr_index: float
    confidence: float
    sector: str
    mvr_dimensions: List[MVRDimension]
    mvr_threshold: bool
    recommendations: List[str]
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
#  Survey Aggregate
# ---------------------------

class StakeholderResponse(BaseModel):
    dimension: str
    scale: float
    reasons: List[str]


class SurveyAggregateRequest(BaseModel):
    stakeholder_responses: List[StakeholderResponse]
    sector: Optional[str] = None


class SurveyAggregateResponse(BaseModel):
    ok: bool
    sector: str
    mvr_index: float
    matrix_axes: Dict[str, float]
    insights: List[str]
    recommendations: List[str]
    summary: str
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Trends
# ---------------------------

class TrendsResponse(BaseModel):
    ok: bool
    sector: str
    days: int
    average_index: float
    slope: float
    interpretation: str
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Forecast
# ---------------------------

class ForecastRequest(BaseModel):
    current_index: float
    velocity: float
    horizon: Optional[int] = None


class ForecastResponse(BaseModel):
    ok: bool
    current_index: float
    projected_index: float
    horizon_days: float
    confidence: float
    pmf_projection: str
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Compare
# ---------------------------

class CompareRequest(BaseModel):
    a_index: float
    b_index: float


class CompareResponse(BaseModel):
    ok: bool
    delta: float
    verdict: str
    policy_trace: Dict[str, Any]
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Benchmark
# ---------------------------

class BenchmarkData(BaseModel):
    average: float
    top_quartile: float
    bottom_quartile: float
    sample_size: int


class BenchmarkResponse(BaseModel):
    ok: bool
    sector: str
    benchmark: BenchmarkData
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Insights
# ---------------------------

class InsightEntity(BaseModel):
    rank: int
    sector: str
    mvr_index: float
    caption: str


class InsightsResponse(BaseModel):
    ok: bool
    sector: str
    top_entities: List[InsightEntity]
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Temperature
# ---------------------------

class TemperatureResponse(BaseModel):
    ok: bool
    date: str
    continent_score: float
    hottest_sector: str
    coolest_sector: str
    region: str
    sample_size: int
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Policy Multi
# ---------------------------

class PolicyAuditResponse(BaseModel):
    ok: bool
    policies_analyzed: int
    compliance_score: float
    recommendations: List[str]
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Story
# ---------------------------

class ImpactMetrics(BaseModel):
    trust_growth: float
    relationship_longevity: float


class StoryResponse(BaseModel):
    ok: bool
    story: str
    impact_metrics: ImpactMetrics
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Meta
# ---------------------------

class MetaResponse(BaseModel):
    ok: bool
    api_name: str
    version: str
    model: str
    endpoints: List[str]
    limits: Dict[str, int]
    last_model_refresh: Optional[str]
    model_fingerprint: Optional[str]
    attribution: AttributionObject


# ---------------------------
# Usage
# ---------------------------

class UsageResponse(BaseModel):
    ok: bool
    plan: str
    date: str
    used_today: float
    daily_limit: float
    attribution: AttributionObject


# ---------------------------
# WhoAmI
# ---------------------------

class WhoAmIResponse(BaseModel):
    ok: bool
    api: str
    version: str
    capabilities: List[str]
    author: str
    region: str
    attribution: AttributionObject


# ---------------------------
# Docs
# ---------------------------

class DocsResponse(BaseModel):
    ok: bool
    documentation: str
    endpoints: List[str]
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Session
# ---------------------------

class SessionResponse(BaseModel):
    ok: bool
    session_token: str
    expires_in: int
    expires_at: str
    plan: str
    version_info: VersionInfo
    attribution: AttributionObject


# ---------------------------
# Health
# ---------------------------

class HealthResponse(BaseModel):
    ok: bool
    service: str
    time: str
    region: str
    performance: str
    security: str
    version: str
    uptime_seconds: float
    features: List[str]
    attribution: AttributionObject


# ---------------------------
# API Error
# ---------------------------

class MVRApiError(BaseModel):
    ok: bool = False
    error: str
    error_code: str
    message: str
    request_id: Optional[str] = None
    limit: Optional[int] = None
    window: Optional[str] = None
    retry_after: Optional[int] = None
    attribution: AttributionObject
