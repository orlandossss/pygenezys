import responses

CHALLENGES_URL = "https://app.genezys.xyz/api-prod-challenge-service/challenges"


@responses.activate
def test_get_challenges_info(client, load_fixture):
    fixture = load_fixture("challenges.json")
    responses.add(responses.GET, CHALLENGES_URL, json=fixture, status=200)

    expected = [
        {
            "name": c["title"],
            "athlete": c["clientName"],
            "total_entries": c["nbTotalEntries"],
            "start_date": c["challengeStartAt"],
            "end_date": c["challengeEndAt"],
        }
        for c in fixture["data"]
    ]
    assert client.challenges.get_challenges_info() == expected
