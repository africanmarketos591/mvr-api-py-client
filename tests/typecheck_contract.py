from mvr_api import CompiledPack, EvidenceItem, FirstCallRequest, RecommendedInputsRequest, define_evidence_item


evidence: EvidenceItem = {
    "id": "EV-1",
    "evidence_type": "survey",
    "evidence_origin": "field_research",
    "source_grade": "B",
    "source_class": "structured_field_research",
    "stakeholder_class": "retailer",
    "collection_method": "structured_interview_protocol",
    "entity_archetype": "retail_chain",
    "guardian_tier": "meso_community",
    "source_confidence": "high",
    "review_status": "verified",
    "privacy_envelope": {"contains_pii": False, "consent_basis": "consent", "retention_class": "90d", "redaction_status": "aggregated"},
    "provenance_ledger": {"extraction_method": "human", "extraction_confidence": 1.0},
    "source_artifacts": [{"artifact_id": "ART-1", "human_reviewed": True, "extraction_method": "human"}],
    "evidence_geography": {"country": "UG", "city": "Kampala"},
    "structured_values": {"trust": 72.0, "permission": 68.0},
}

compiled_pack: CompiledPack = {"survey_pack": [evidence]}
first_call: FirstCallRequest = {
    "subject": {"entity_name": "Example venture", "entity_archetype": "generic_startup", "custom_discovery_hint": "early"},
    "entity_archetype": "generic_startup",
    "market_scope": {"country": "UG", "sector": "supplier finance"},
}
recommended_inputs: RecommendedInputsRequest = {"endpoint": "/v1/decision-check", "entity_archetype": "fintech_lending"}

bad_evidence_type: EvidenceItem = {"evidence_type": "blog_post"}  # type: ignore
bad_recommended_archetype: RecommendedInputsRequest = {"entity_archetype": "generic_startup"}  # type: ignore
bad_source_class: EvidenceItem = {"source_class": "blog"}  # type: ignore
bad_stakeholder_class: EvidenceItem = {"stakeholder_class": "random_person"}  # type: ignore
bad_collection_method: EvidenceItem = {"collection_method": "scraped_guess"}  # type: ignore
bad_consent_basis: EvidenceItem = {"privacy_envelope": {"consent_basis": "assumed"}}  # type: ignore
bad_provenance_method: EvidenceItem = {"provenance_ledger": {"extraction_method": "human_verified"}}  # type: ignore
bad_artifact_method: EvidenceItem = {"source_artifacts": [{"extraction_method": "ocr_magic"}]}  # type: ignore
bad_compiled_pack: CompiledPack = {"unexpected_pack": []}  # type: ignore

extended_evidence: EvidenceItem = define_evidence_item({
    "id": "EV-EXT-1",
    "evidence_type": "public_filing",
    "source_class": "regulator_published",
    "custom_signal": {"registry_match": True},
})

_ = (compiled_pack, first_call, recommended_inputs, bad_evidence_type, bad_recommended_archetype, bad_source_class, bad_stakeholder_class, bad_collection_method, bad_consent_basis, bad_provenance_method, bad_artifact_method, bad_compiled_pack, extended_evidence)
