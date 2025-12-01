# African Market OS — AMOS-MVR API Python Client

Official **Python SDK** for the  
**African Market OS – AMOS Relational Porosity & MVR API (v1.0.0)**

This client provides convenient access to the public AMOS-MVR API endpoints:

- ✔ AMOS relational risk scoring & safe credit limits (`POST /v1/amos/score`)
- ✔ Engine health & metadata (`GET /health`)

It is a thin wrapper around the HTTP API, with:

- Typed request/response models for **AMOSScoreRequest** and **AMOSScoreResponse**
- Automatic injection of required headers:
  - `x-mvr-license` (license key)
  - `x-buyer-email` (buyer email for governance / audit)
- Basic error handling that surfaces structured `AMOSErrorResponse` payloads

---

## 📦 Installation

From PyPI (recommended):

```bash
pip install mvr-api-client
Or from source (inside the repo):pip install .

🚀 Quickstart: Score an Entity with AMOS-MVR API
from mvr_api import AMOSClient, AMOSConfig, AMOSScoreRequest

# 1. Create configuration
config = AMOSConfig(
    license_key="your-license-key",          # maps to x-mvr-license
    buyer_email="you@example.com",          # maps to x-buyer-email
    base_url="https://africanmarketos.com", # optional override
    timeout=30.0                             # optional: request timeout in seconds
)

# 2. Initialize client
client = AMOSClient(config)

# 3. Build a minimal AMOS score request
request = AMOSScoreRequest(
    amos_id="EXAMPLE_FINTECH_ANCHOR_001",
    sector="FINTECH",
    region="EA",
    revenue=307142100000,
    cash=22098100000,
    days_silent=1,
    occupancy_rate=97,
    collection_rate=97,
    currency="KES"
    # Optional: add total_debt, arrears, fx_exposed_debt, mvr block, etc.
)

# 4. Call the scoring endpoint
response = client.score_amos(request)

print("RRS_SCORE:", response.RRS_SCORE)
print("Pz_POROSITY:", response.Pz_POROSITY)
print("MVR_I:", response.meta.MVR_I)
print("Safe credit limit (local):", response.CREDIT_ENGINE.ESTIMATED_SAFE_CREDIT_LIMIT_LOCAL)
print("Recommended action:", response.CREDIT_ENGINE.RECOMMENDED_ACTION)

🧪 Example: Including Explicit MVR Scores

If you already have relational / survey-derived scores (MVR-I, embeddedness, trust, etc.),
you can pass them explicitly instead of letting AMOS infer them:
from mvr_api import AMOSScoreRequest, MVRBlock

request = AMOSScoreRequest(
    amos_id="ANCHOR_WITH_SURVEY_DATA",
    sector="FMCG_BEVERAGE",
    region="EA",
    revenue=2900000000000,
    cash=170000000000,
    days_silent=2,
    occupancy_rate=98,
    collection_rate=96,
    currency="KES",
    mvr=MVRBlock(
        mvr_i=80,
        embeddedness=82,
        trust=81,
        reciprocity=78,
        guardian_vouchers=80,
        continuity=82,
        channel_permission=76,
        cultural_fit=79,  # optional field
    ),
)
response = client.score_amos(request)
print("MVR band:", response.meta.MVR_BAND)
print("Headline:", response.meta.HEADLINE)

❤️ Health Check / Engine Metadata

You can ping the engine and retrieve basic metadata:
from mvr_api import AMOSClient, AMOSConfig

config = AMOSConfig(
    license_key="your-license-key",
    buyer_email="you@example.com",
)

client = AMOSClient(config)
health = client.get_health()  # wraps GET /health

print("Status:", health.status)
print("Engine version:", health.version)
print("Wrapper:", health.wrapper)
print("Timestamp:", health.timestamp)

🛡 Error Handling
All API errors are surfaced as a structured AMOSApiError, which wraps the
server’s AMOSErrorResponse:
from mvr_api import AMOSClient, AMOSConfig, AMOSScoreRequest, AMOSApiError

config = AMOSConfig(
    license_key="your-license-key",
    buyer_email="you@example.com",
)
client = AMOSClient(config)

try:
    request = AMOSScoreRequest(
        amos_id="MISSING_REQUIRED_FIELDS_EXAMPLE",
        sector="FINTECH",
        region="EA",
        # intentionally omitting required fields like revenue, cash, etc.
        revenue=0,
        cash=0,
        days_silent=0,
        occupancy_rate=0,
        collection_rate=0,
    )
    response = client.score_amos(request)
except AMOSApiError as e:
    # e.error_data should mirror AMOSErrorResponse
    print("Error:", e.error_data.error)
    print("Request ID:", e.error_data.request_id)
    print("Details:", e.error_data.details)
You can use request_id when talking to African Market OS support to trace specific calls.

📂 Project Structure
mvr-api-py-client/
│
├── setup.py
├── README.md
└── mvr_api/
    ├── __init__.py
    ├── client.py        # AMOSClient, AMOSConfig, low-level HTTP helpers
    └── models.py        # AMOSScoreRequest, AMOSScoreResponse, AMOSMeta, etc.
The models.py definitions are aligned with the AMOS-MVR OpenAPI spec v1.0.0
(AMOSScoreRequest, AMOSScoreResponse, AMOSMeta, CreditEngineBlock,
WrapperBlock, ModelMetadata, AMOSErrorResponse, HealthResponse, …).

📄 License
This SDK is released under the MIT License.
You are free to use it in commercial and non-commercial projects, subject to the license.
Note: Access to the AMOS-MVR API itself still requires a valid license key and
is governed by the African Market OS commercial / referral use policy.

🧬 Attribution
Minimum Viable Relationships (MVR) Framework • African Market OS
Creator: Farouk Mark Mukiibi
Framework DOI: 10.5281/zenodo.17310446
If you use AMOS or the MVR framework in academic work, please cite the DOI above.

🌍 About AMOS & MVR

The Minimum Viable Relationships (MVR) Framework and AMOS Relational Porosity Engine measure relational readiness and relational risk using:

Trust & reciprocity

Belonging & embeddedness

Permission & cultural-market fit

Guardian vouchers and community guardianship

Network health, arrears / leakage, and cash runway

The AMOS-MVR API is optimized for:

African trade credit

Embedded fintech & FMCG corridors

Situations where relational credit and community context matter as much as balance sheets.

Learn more:
https://africanmarketos.com/the-mvr-framework-minimum-viable-relationships/
