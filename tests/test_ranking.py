import responses

CUP_RANKING_URL = "https://app.genezys.xyz/api-prod-leaderboard-service/rankings/cup/overview"
DIVISION_RANKING_URL = "https://app.genezys.xyz/api-prod-leaderboard-service/rankings/division/overview"


def _expected_player(p):
    return {
        "score": p["score"],
        "name": p["pseudo"],
        "userId": p["userId"],
        "matchplayed": p["nbMatchLaunch"],
        "position": p["position"],
    }


@responses.activate
def test_cup_leaderboard(client, load_fixture):
    fixture = load_fixture("ranking_cup_overview.json")
    responses.add(responses.GET, CUP_RANKING_URL, json=fixture, status=200)

    own_info, players = client.ranking.cup_leaderboard("cup-123", 5)

    me = fixture["data"]["me"]
    assert own_info == {
        "score": me["score"],
        "matchplayed": me["nbMatchLaunch"],
        "position": me["position"],
    }
    assert players == [_expected_player(p) for p in fixture["data"]["top"]]


@responses.activate
def test_division_leaderboard(client, load_fixture):
    fixture = load_fixture("ranking_division_overview.json")
    responses.add(responses.GET, DIVISION_RANKING_URL, json=fixture, status=200)

    own_info, players = client.ranking.division_leaderboard(5)

    me = fixture["data"]["me"]
    assert own_info == {
        "score": me["score"],
        "matchplayed": me["nbMatchLaunch"],
        "position": me["position"],
        "division_rank": me["divisionRank"],
    }
    assert players == [_expected_player(p) for p in fixture["data"]["top"]]
