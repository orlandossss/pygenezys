import responses

ARENA_URL = "https://app.genezys.xyz/api-prod-fantasy-game-service/arenatheme/current"


@responses.activate
def test_get_arena_info(client, load_fixture):
    fixture = load_fixture("arena_current.json")
    responses.add(responses.GET, ARENA_URL, json=fixture, status=200)

    name, category, attribut = client.arena.get_arena_info()

    assert name == fixture["data"]["title"]
    assert category == fixture["data"]["levels"]
    assert attribut == fixture["data"]["characteristics"]
