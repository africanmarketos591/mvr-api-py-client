import unittest
from unittest.mock import Mock

from mvr_api import MVRApiError, MVRClient, MVRConfig, define_evidence_item


class ClientContractTests(unittest.TestCase):
    def setUp(self):
        self.client = MVRClient(MVRConfig(base_url="https://example.test", api_key="test-key", max_retries=0))
        self.request = Mock()
        self.client.session.request = self.request

    @staticmethod
    def response(status_code=200, payload=None, headers=None):
        result = Mock()
        result.status_code = status_code
        result.headers = headers or {}
        result.json.return_value = payload or {"status": "ok"}
        result.text = ""
        return result

    def test_certified_helpers_preserve_route_body_and_headers(self):
        self.request.side_effect = [self.response(), self.response(), self.response()]

        self.client.first_call({"entity": "Example", "country": "UG", "question": "Should it launch?"})
        self.client.recommended_inputs({"endpoint": "/v1/decision-check", "entity_archetype": "distributor_network"})
        self.client.remediation_path({"decision_result": {"status": "abstained"}, "target_verdict": "pilot_only"})

        calls = self.request.call_args_list
        self.assertEqual([call.args[1] for call in calls], [
            "https://example.test/v1/first-call",
            "https://example.test/v1/recommended-inputs",
            "https://example.test/v1/remediation-path",
        ])
        self.assertEqual(calls[0].kwargs["json"]["question"], "Should it launch?")
        self.assertEqual(calls[1].kwargs["json"]["entity_archetype"], "distributor_network")
        self.assertEqual(calls[2].kwargs["json"]["target_verdict"], "pilot_only")
        self.assertEqual(self.client.session.headers["X-API-Key"], "test-key")
        self.assertEqual(self.client.session.headers["X-Response-Profile"], "full_advisory")
        self.assertTrue(self.client.session.headers["User-Agent"].endswith("6.32.3"))

    def test_structured_http_error_is_preserved(self):
        self.request.return_value = self.response(
            422,
            {"error": "Utility validation failed", "details": ["target_verdict must be canonical"]},
        )

        with self.assertRaises(MVRApiError) as caught:
            self.client.remediation_path({"decision_result": {}, "target_verdict": "pilot_only"})

        self.assertEqual(caught.exception.status_code, 422)
        self.assertEqual(caught.exception.error_data["error"], "Utility validation failed")

    def test_extension_helper_preserves_custom_fields_and_rejects_invalid_known_enums(self):
        item = define_evidence_item({
            "id": "EV-EXT-1",
            "evidence_type": "public_filing",
            "custom_signal": {"registry_match": True},
        })
        self.assertEqual(item["custom_signal"], {"registry_match": True})

        with self.assertRaisesRegex(ValueError, "privacy_envelope.consent_basis"):
            define_evidence_item({"privacy_envelope": {"consent_basis": "assumed"}})
        with self.assertRaisesRegex(ValueError, "provenance_ledger.extraction_method"):
            define_evidence_item({"provenance_ledger": {"extraction_method": "human_verified"}})
        with self.assertRaisesRegex(ValueError, r"source_artifacts\[0\].extraction_method"):
            define_evidence_item({"source_artifacts": [{"extraction_method": "ocr_magic"}]})


if __name__ == "__main__":
    unittest.main()
