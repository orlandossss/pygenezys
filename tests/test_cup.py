import responses

CUPS_URL = "https://app.genezys.xyz/api-prod-fantasy-game-service/cups"


@responses.activate
def test_get_available_cups_id(client, load_fixture):
    fixture = load_fixture("cups.json")
    responses.add(responses.GET, CUPS_URL, json=fixture, status=200)
    assert client.cup.get_available_cups_id() == [cup["id"] for cup in fixture["data"]]


@responses.activate
def test_get_available_cups_info(client, load_fixture):
    fixture = load_fixture("cups.json")
    responses.add(responses.GET, CUPS_URL, json=fixture, status=200)
    expected = [
        {"id": cup["id"], "accepted_rarities": cup["constraints"]["acceptedRarities"]}
        for cup in fixture["data"]
    ]
    assert client.cup.get_available_cups_info() == expected


@responses.activate
def test_get_all_info(client, load_fixture):
    fixture = load_fixture("cups.json")
    responses.add(responses.GET, CUPS_URL, json=fixture, status=200)
    assert client.cup.get_all_info() == fixture
