from __future__ import annotations

import os
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

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


EntityArchetype = Literal[
    "telecom_operator", "mobile_money_operator", "fintech_platform", "financial_services_bank",
    "fintech_lending", "logistics_platform", "energy_utility", "extractives_operator",
    "real_estate_construction", "education_provider", "passenger_mobility", "b2b_saas_platform",
    "healthtech_platform", "insurance_platform", "fmcg_brand", "retail_chain", "ecommerce_platform",
    "manufacturer", "distributor_network", "ngo", "development_program", "public_institution",
    "survey_dataset", "solo_entrepreneur", "family_business", "cooperative_sacco",
    "cross_border_trader", "university_spinout", "diaspora_venture", "creator_economy_individual",
    "agritech_aggregator", "impact_enterprise", "religious_institution", "chama_savings_group",
]

MVRVerdict = Literal["permission_not_yet_earned", "pilot_only", "pilot_ready", "ready_to_scale"]
StringOrStringList = Union[str, List[str]]

EvidenceType = Literal[
    "public_filing", "survey", "interview", "observation", "telemetry", "admin_data",
    "evaluation", "retail_audit", "social_listening", "partner_network", "program_monitoring",
]
EvidenceOrigin = Literal["public_osint", "field_research", "mixed", "corporate_telemetry", "platform_telemetry"]
SourceGrade = Literal["A", "B", "C", "D"]


class MVRSubject(TypedDict, total=False):
    entity_name: str
    name: str
    country: str
    entity_archetype: EntityArchetype
    category: str


class MVRMarketScope(TypedDict, total=False):
    country: str
    sector: str
    city: str
    town_or_zone: str
    region: str
    analysis_date: str
    evaluation_date: str


class EvidenceItem(TypedDict, total=False):
    id: str
    evidence_type: EvidenceType
    evidence_origin: EvidenceOrigin
    source_grade: SourceGrade
    source_class: str
    entity_archetype: EntityArchetype
    stakeholder_class: str
    collection_method: str
    freshness_date: str
    evidence_geography: MVRMarketScope
    structured_values: Dict[str, float]
    provenance_ledger: Dict[str, Any]
    survey_payload: Dict[str, Any]
    program_payload: Dict[str, Any]
    admin_data_payload: Dict[str, Any]
    retail_audit_payload: Dict[str, Any]


class CompiledPack(TypedDict, total=False):
    public_reality_pack: List[EvidenceItem]
    telemetry_proxy_pack: List[EvidenceItem]
    localized_observed_pack: List[EvidenceItem]
    survey_pack: List[EvidenceItem]
    retail_audit_pack: List[EvidenceItem]
    ngo_program_pack: List[EvidenceItem]
    administrative_data_pack: List[EvidenceItem]
    evaluation_pack: List[EvidenceItem]
    partner_network_pack: List[EvidenceItem]
    social_listening_pack: List[EvidenceItem]


class FirstCallRequest(TypedDict, total=False):
    subject: MVRSubject
    market_scope: MVRMarketScope
    entity: str
    entity_name: str
    company_name: str
    company: str
    name: str
    query: str
    country: str
    sector: str
    industry: str
    entity_archetype: EntityArchetype
    use_case: str
    question: str
    intent: str
    decision: str
    intended_action: str
    decision_context: str
    stage: str
    target_users: str
    evidence_available: StringOrStringList
    evidence_types: StringOrStringList
    sources: StringOrStringList
    known_partners: StringOrStringList
    partners: StringOrStringList
    channels: StringOrStringList
    evidence_pack: List[EvidenceItem]
    evidence_items: List[EvidenceItem]
    city: str
    town_or_zone: str


class RecommendedInputsRequest(TypedDict, total=False):
    endpoint: str
    route: str
    path: str
    entity_archetype: EntityArchetype
    category: str
    subject: MVRSubject
    country: str
    goal: str
    evidence_maturity: str


class RemediationPathRequest(TypedDict, total=False):
    decision_result: Dict[str, Any]
    subject: MVRSubject
    market_scope: MVRMarketScope
    evidence_pack: List[EvidenceItem]
    compiled_pack: CompiledPack
    target_verdict: MVRVerdict
    audience: str
    gap_plan: Dict[str, Any]
    evidence_run: Dict[str, Any]
    evidence_recruitment_plan: Dict[str, Any]
    mvr_result: Dict[str, Any]
    decision_room: Dict[str, Any]
    red_team: Dict[str, Any]
    release_check: Dict[str, Any]
    project_id: str


class EvidenceCompletenessRequest(TypedDict, total=False):
    subject: MVRSubject
    market_scope: MVRMarketScope
    evidence_pack: List[EvidenceItem]
    compiled_pack: CompiledPack
    stakeholder_scope: List[str]
    target_verdict: MVRVerdict


class ContextCompileRequest(TypedDict, total=False):
    subject: MVRSubject
    market_scope: MVRMarketScope
    evidence_pack: List[EvidenceItem]
    compiled_pack: CompiledPack
    analysis_date: str
    requested_use: str


class DecisionCheckRequest(TypedDict, total=False):
    mode: Literal["exploratory", "evidence_backed", "compiled_evidence"]
    subject: MVRSubject
    market_scope: MVRMarketScope
    evidence_pack: List[EvidenceItem]
    compiled_pack: CompiledPack
