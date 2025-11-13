from mvr_api import MVRClient

def example():
    client = MVRClient(
        license="your-license-key",
        email="your@email.com"
    )

    # Health check
    print("Checking API health...")
    health = client.health()
    print("API Status:", health.ok, "Region:", health.region)

    # Fetch MVR Scores
    print("\nFetching Scores...")
    scores = client.get_scores("fintech")
    print("MVR Index:", scores.mvr_index)

    # Submit Survey
    print("\nSubmitting Survey Aggregate...")
    survey = client.survey_aggregate({
        "stakeholder_responses": [
            {
                "dimension": "Embeddedness",
                "scale": 4,
                "reasons": ["Strong community integration"]
            }
        ],
        "sector": "fintech"
    })
    print("Survey MVR Index:", survey.mvr_index)

    # Create Session Token
    print("\nCreating Session...")
    session = client.create_session("your-license-key", "your@email.com")
    print("Session Token:", session.session_token)

    print("\nDone.")

if __name__ == "__main__":
    example()
