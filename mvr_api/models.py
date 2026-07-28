from __future__ import annotations

import os
from typing import Any, Dict, List, Literal, Mapping, Optional, TypedDict, Union, cast, get_args

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
SourceClass = Literal[
    "entity_reported", "independently_audited", "regulator_published", "administrative_record",
    "probability_sample_survey", "nonprobability_survey", "structured_field_research",
    "third_party_evaluation", "retail_audit", "telemetry_internal", "media_reported", "model_inferred",
]
StakeholderClass = Literal[
    "agent", "anchor_customer", "bank_lender", "beneficiary", "board", "board_member", "chama_member",
    "channel_gatekeeper", "chief", "civil_society_org", "clinic", "community_guardian", "community_leader",
    "competitor", "competitors", "consumer", "cooperative_member", "court", "courts", "creditor", "creditors",
    "customary_land_authority", "customer", "customs", "customs_authority", "distributor", "donor",
    "donor_guardian", "enumerator", "farmer", "field_agent", "field_supervisor", "gatekeeper", "guarantor",
    "guardian", "guardian_node", "implementing_partner", "incumbent", "incumbent_competitor", "incumbents",
    "influencer", "informal_logistics", "informal_logistics_partner", "institutional_guardian",
    "internal_operations", "internal_operator", "investor", "investor_board", "investors", "journalist",
    "journalists", "judiciary", "judiciary_court", "labor_union", "labour_union", "land_custodian",
    "land_owner", "landlord", "landowner", "lender", "lender_creditor", "lenders", "market_queen", "media",
    "media_press", "member", "micro_logistics", "mobile_money_agent", "organized_labour", "platform_partner",
    "political_guardian", "press", "public_official", "regulator", "regulatory_body", "religious_leader",
    "research_respondent_group", "retail_partner", "retailer", "retailer_partner", "revenue_authority",
    "sacco_member", "school", "service_provider", "shareholder", "shareholders", "supplier", "suppliers",
    "tax_authority", "tax_revenue_authority", "teacher", "traditional_chief", "union", "upstream_supplier",
    "upstream_vendor", "vc", "vendor", "vendors", "venture_capital", "worker_association", "works_council",
]
CollectionMethod = Literal[
    "structured_interview_protocol", "expert_ethnographic_observation", "field_observation",
    "survey_platform_verified", "survey_paper_based", "key_informant_interview", "team_consensus_estimate",
    "founder_intuition", "inferred_from_secondary", "direct", "inferred", "secondary_source",
    "corporate_telemetry", "database_aggregation", "expert_opinion", "intercept_interview",
]
GuardianTier = Literal["macro_regulator", "meso_community", "micro_street"]
SourceConfidence = Literal["high", "medium", "low"]
ReviewStatus = Literal["pending", "approved", "accepted", "verified", "reviewed", "rejected"]
PublicMetricScope = Literal["entity_scale", "country_scale", "regional_scale", "city_scale", "site_scale"]
ProvenanceExtractionMethod = Literal["human", "deterministic_parser", "llm_inferred", "automated_query"]
PrivacyConsentBasis = Literal[
    "consent", "contract", "legitimate_interest", "public_interest", "legal_obligation", "not_applicable",
]
PrivacyRetentionClass = Literal["session_only", "30d", "90d", "1y", "7y", "contractual"]
PrivacyRedactionStatus = Literal["raw", "minimized", "redacted", "aggregated"]


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


class PrivacyEnvelope(TypedDict, total=False):
    contains_pii: bool
    contains_sensitive_personal_data: bool
    consent_basis: PrivacyConsentBasis
    retention_class: PrivacyRetentionClass
    redaction_status: PrivacyRedactionStatus
    safe_for_modeling: bool


class ProvenanceLedger(TypedDict, total=False):
    source_family: str
    source_doc_id: str
    source_locator: str
    extraction_method: ProvenanceExtractionMethod
    extraction_confidence: float
    compiler_stage: str
    data_integrity: Dict[str, Any]


class SourceArtifact(TypedDict, total=False):
    artifact_id: str
    media_type: str
    storage_uri: str
    sha256: str
    extraction_method: ProvenanceExtractionMethod
    extractor_version: str
    extracted_at: str
    human_reviewed: bool


class EvidenceItem(TypedDict, total=False):
    id: str
    evidence_id: str
    evidence_type: EvidenceType
    evidence_origin: EvidenceOrigin
    source_grade: SourceGrade
    source_class: SourceClass
    entity_archetype: EntityArchetype
    stakeholder_class: StakeholderClass
    guardian_tier: GuardianTier
    collection_method: CollectionMethod
    source_confidence: SourceConfidence
    freshness_date: str
    evidence_geography: MVRMarketScope
    geography: MVRMarketScope
    temporal: Dict[str, Any]
    public_metric_scope: PublicMetricScope
    public_metrics: Dict[str, Any]
    structured_values: Dict[str, float]
    structured_values_scale: str
    behavioral_values: Dict[str, Any]
    structured_values_provenance: Dict[str, Any]
    human_reviewed: bool
    review_status: ReviewStatus
    reviewed_by: str
    reviewed_at: str
    human_review: Dict[str, Any]
    organ_attestation: Dict[str, Any]
    _verifier_attestation: Dict[str, Any]
    privacy_envelope: PrivacyEnvelope
    uncertainty_envelope: Dict[str, Any]
    provenance_ledger: ProvenanceLedger
    survey_payload: Dict[str, Any]
    program_payload: Dict[str, Any]
    admin_data_payload: Dict[str, Any]
    retail_audit_payload: Dict[str, Any]
    source_artifacts: List[SourceArtifact]


_EVIDENCE_ENUMS = {
    "evidence_type": set(get_args(EvidenceType)),
    "evidence_origin": set(get_args(EvidenceOrigin)),
    "source_grade": set(get_args(SourceGrade)),
    "source_class": set(get_args(SourceClass)),
    "entity_archetype": set(get_args(EntityArchetype)),
    "stakeholder_class": set(get_args(StakeholderClass)),
    "guardian_tier": set(get_args(GuardianTier)),
    "collection_method": set(get_args(CollectionMethod)),
    "source_confidence": set(get_args(SourceConfidence)),
    "review_status": set(get_args(ReviewStatus)),
    "public_metric_scope": set(get_args(PublicMetricScope)),
}
_PROVENANCE_METHODS = set(get_args(ProvenanceExtractionMethod))
_PRIVACY_ENUMS = {
    "consent_basis": set(get_args(PrivacyConsentBasis)),
    "retention_class": set(get_args(PrivacyRetentionClass)),
    "redaction_status": set(get_args(PrivacyRedactionStatus)),
}


def define_evidence_item(item: Mapping[str, Any]) -> EvidenceItem:
    """Preserve extension fields while validating every published enum present in the item."""

    result = dict(item)
    for field, allowed in _EVIDENCE_ENUMS.items():
        value = result.get(field)
        if value is not None and value not in allowed:
            raise ValueError(f"{field} must be one of: {', '.join(sorted(allowed))}")

    privacy = result.get("privacy_envelope")
    if privacy is not None:
        if not isinstance(privacy, Mapping):
            raise ValueError("privacy_envelope must be a mapping")
        for field, allowed in _PRIVACY_ENUMS.items():
            value = privacy.get(field)
            if value is not None and value not in allowed:
                raise ValueError(f"privacy_envelope.{field} must be one of: {', '.join(sorted(allowed))}")

    provenance = result.get("provenance_ledger")
    if provenance is not None:
        if not isinstance(provenance, Mapping):
            raise ValueError("provenance_ledger must be a mapping")
        method = provenance.get("extraction_method")
        if method is not None and method not in _PROVENANCE_METHODS:
            raise ValueError("provenance_ledger.extraction_method must use the published extraction-method enum")

    artifacts = result.get("source_artifacts")
    if artifacts is not None:
        if not isinstance(artifacts, list):
            raise ValueError("source_artifacts must be a list")
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, Mapping):
                raise ValueError(f"source_artifacts[{index}] must be a mapping")
            method = artifact.get("extraction_method")
            if method is not None and method not in _PROVENANCE_METHODS:
                raise ValueError(f"source_artifacts[{index}].extraction_method must use the published extraction-method enum")

    return cast(EvidenceItem, result)


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
    subject: Dict[str, Any]
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
