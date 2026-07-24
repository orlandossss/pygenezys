import responses

DIVISION_MATCH_URL = "https://app.genezys.xyz/api-prod-fantasy-game-service/match/division/new"
CUP_MATCH_URL = "https://app.genezys.xyz/api-prod-fantasy-game-service/match/cup/new"


@responses.activate
def test_run_division_match(client, load_fixture):
    fixture = load_fixture("match_division_new.json")
    responses.add(responses.GET, DIVISION_MATCH_URL, json=fixture, status=200)
    assert client.match.run_division_match() == fixture


@responses.activate
def test_run_cup_match(client, load_fixture):
    fixture = load_fixture("match_cup_new.json")
    responses.add(responses.GET, CUP_MATCH_URL, json=fixture, status=200)
    assert client.match.run_cup_match("cup-123") == fixture
