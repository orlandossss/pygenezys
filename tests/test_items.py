import pytest
import responses

ITEMS_URL = "https://app.genezys.xyz/api-prod-fantasy-game-service/items"


@responses.activate
def test_get_all_info(client, load_fixture):
    fixture = load_fixture("items.json")
    responses.add(responses.GET, ITEMS_URL, json=fixture, status=200)

    assert client.items.get_all_info() == fixture


@responses.activate
def test_get_items_info(client, load_fixture):
    fixture = load_fixture("items.json")
    responses.add(responses.GET, ITEMS_URL, json=fixture, status=200)

    result = client.items.get_items_info()

    assert result == [
        {
            "id": "1f09e079-8f83-6b50-a63c-3214d527559e_f4487c107fb73b560f3242817e12db58",
            "type": "consumable",
            "title": "Boisson énergétisante ⚡",
            "quantity": 10,
            "in_nb_deck_usage": 0,
            "health_points": 50,
            "boosted_characteristics": [],
        },
        {
            "id": "1f09e0bd-e101-6470-ec79-2c9d42f67a39_ee9a8b9755c8e1670ec0be4da458e65e",
            "type": "equipment",
            "title": "Basket 👟",
            "quantity": 1,
            "in_nb_deck_usage": 4,
            "health_points": None,
            "boosted_characteristics": [
                {"name": "Power", "boost_percentage": 10},
                {"name": "Endurance", "boost_percentage": 5},
                {"name": "Reflexes", "boost_percentage": -10},
            ],
        },
    ]


@responses.activate
def test_get_items_info_filters_by_type(client, load_fixture):
    fixture = load_fixture("items.json")
    responses.add(responses.GET, ITEMS_URL, json=fixture, status=200)

    result = client.items.get_items_info(item_type="equipment")

    assert len(result) == 1
    assert result[0]["type"] == "equipment"


def test_get_items_info_invalid_type_raises(client):
    with pytest.raises(ValueError):
        client.items.get_items_info(item_type="not-a-real-type")
