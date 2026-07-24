import responses

MY_CARDS_URL = "https://app.genezys.xyz/api-prod-collection-service/cards"


@responses.activate
def test_get_my_cards(client, load_fixture):
    fixture = load_fixture("my_cards_summary.json")
    responses.add(responses.GET, MY_CARDS_URL, json=fixture, status=200)
    assert client.my_cards.get_my_cards() == fixture
