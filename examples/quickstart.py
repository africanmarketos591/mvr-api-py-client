from mvr_api import (
    AMOSApiClient,
    AMOSApiError,
    MVRApiConfig,
    AMOSScoreRequest,
)


def example():
    # Configure the client
    config = MVRApiConfig(
        license="your-license-key",
        email="your@email.com",
        base_url="https://africanmarketos.com",  # AMOS Production Gateway
    )

    client = AMOSApiClient(config)

    # -----------------------------
    # 1) Health check
    # -----------------------------
    print("Checking AMOS API health...")
    health = client.health()
    print("Status:", health.status)
    print("Core version:", health.version)
    print("Wrapper version:", health.wrapper)
    print("Request ID:", health.request_id)
    print()

    # -----------------------------
    # 2) AMOS Relational Risk Score
    # -----------------------------
    print("Requesting AMOS score...")

    # Minimal valid request (see OpenAPI for all optional fields)
    score_request = AMOSScoreRequest(
        amos_id="EXAMPLE_ENTITY_001",
        sector="FMCG_BEVERAGE",
        region="EA",
        revenue=1_000_000_000,
        cash=100_000_000,
        days_silent=2,
        occupancy_rate=95,
        collection_rate=96,
    )

    try:
        result = client.score(score_request)

        print("RRS_SCORE:", result.RRS_SCORE)
        print("Pz_POROSITY:", result.Pz_POROSITY)
        print("MVR-I:", result.meta.MVR_I)
        print("MVR band:", result.meta.MVR_BAND)
        print("Headline:", result.meta.HEADLINE)
        print("Safe Credit Limit (Local):", result.CREDIT_ENGINE.ESTIMATED_SAFE_CREDIT_LIMIT_LOCAL)
        print("Safe Credit Limit (USD):", result.CREDIT_ENGINE.ESTIMATED_SAFE_CREDIT_LIMIT_USD)
        print("Recommended Action:", result.CREDIT_ENGINE.RECOMMENDED_ACTION)

    except AMOSApiError as e:
        print("AMOS API Error:")
        print("  Error:", e.error_data.error)
        details = getattr(e.error_data, "details", None)
        if details:
            print("  Details:", details)
        print("  Request ID:", getattr(e.error_data, "request_id", None))

    print("\nDone.")


if __name__ == "__main__":
    example()
