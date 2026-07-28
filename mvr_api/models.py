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


class FirstCallRequest(TypedDict, total=False):
    subject: Dict[str, Any]
    market_scope: Dict[str, Any]
    entity: str
    entity_name: str
    company_name: str
    company: str
    name: str
    query: str
    country: str
    sector: str
    industry: str
    entity_archetype: str
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
    evidence_pack: List[Dict[str, Any]]
    evidence_items: List[Dict[str, Any]]
    city: str
    town_or_zone: str


class RecommendedInputsRequest(TypedDict, total=False):
    endpoint: str
    route: str
    path: str
    entity_archetype: EntityArchetype
    category: str
    subject: Dict[str, Any]
    country: str
    goal: str
    evidence_maturity: str


class RemediationPathRequest(TypedDict, total=False):
    decision_result: Dict[str, Any]
    subject: Dict[str, Any]
    market_scope: Dict[str, Any]
    evidence_pack: List[Dict[str, Any]]
    compiled_pack: Dict[str, Any]
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
