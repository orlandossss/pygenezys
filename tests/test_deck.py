import responses

USER_URL = "https://app.genezys.xyz/api-prod-user-service/users/connected"
DECK_URL = "https://app.genezys.xyz/api-prod-fantasy-game-service/decks"

CARD_INFO = [
    {"id": "card-1", "collectionId": "coll-1"},
    {"id": "card-2", "collectionId": "coll-2", "equipmentId": "equip-1"},
]


def _mock_user_and_deck(load_fixture):
    responses.add(responses.GET, USER_URL, json=load_fixture("user_connected.json"), status=200)
    responses.add(responses.PUT, DECK_URL, json=load_fixture("deck_build_response.json"), status=200)


@responses.activate
def test_build_deck_division(client, load_fixture):
    _mock_user_and_deck(load_fixture)
    result = client.deck.build_deck_division(CARD_INFO)
    assert result == load_fixture("deck_build_response.json")["message"]


@responses.activate
def test_build_deck_commun_cup(client, load_fixture):
    _mock_user_and_deck(load_fixture)
    result = client.deck.build_deck_commun_cup(CARD_INFO)
    assert result == load_fixture("deck_build_response.json")["message"]


@responses.activate
def test_build_deck_limited_cup(client, load_fixture):
    _mock_user_and_deck(load_fixture)
    result = client.deck.build_deck_limited_cup(CARD_INFO)
    assert result == load_fixture("deck_build_response.json")["message"]


@responses.activate
def test_build_deck_rare_cup(client, load_fixture):
    _mock_user_and_deck(load_fixture)
    result = client.deck.build_deck_rare_cup(CARD_INFO)
    assert result == load_fixture("deck_build_response.json")["message"]


@responses.activate
def test_build_deck_epic_cup(client, load_fixture):
    _mock_user_and_deck(load_fixture)
    result = client.deck.build_deck_epic_cup(CARD_INFO)
    assert result == load_fixture("deck_build_response.json")["message"]


@responses.activate
def test_build_deck_legendary_cup(client, load_fixture):
    _mock_user_and_deck(load_fixture)
    result = client.deck.build_deck_legendary_cup(CARD_INFO)
    assert result == load_fixture("deck_build_response.json")["message"]
