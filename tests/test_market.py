import responses

MARKET_URL = "https://app.genezys.xyz/api-prod-marketplace-service/listings"


@responses.activate
def test_get_market(client, load_fixture):
    fixture = load_fixture("market_summary.json")
    responses.add(responses.GET, MARKET_URL, json=fixture, status=200)
    assert client.market.get_market() == fixture
