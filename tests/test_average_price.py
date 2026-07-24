import responses

PRICES_URL = "https://app.genezys.xyz/api-prod-marketplace-service/stats/rarity-sale-prices"


@responses.activate
def test_average_prices(client, load_fixture):
    fixture = load_fixture("average_prices.json")
    responses.add(responses.GET, PRICES_URL, json=fixture, status=200)

    expected = {p["rarity"]: p["averagePrice"] for p in fixture["data"]["averagePrices"]}
    limited, rare, epic, legendary = client.average_price.average_prices()

    assert limited == expected["Limited"]
    assert rare == expected["Rare"]
    assert epic == expected["Epic"]
    assert legendary == expected["Legendary"]
