import responses

MATCH_HISTORY_URL = "https://app.genezys.xyz/api-prod-fantasy-game-service/match/division"


def _expected_deck(cards_equipments):
    return [
        {
            "card_name": c["card"]["clientName"],
            "score": c["score"],
            "health": c["card"]["health"]["points"],
        }
        for c in cards_equipments
    ]


@responses.activate
def test_get_match_history(client, load_fixture):
    fixture = load_fixture("match_division_history.json")
    responses.add(responses.GET, MATCH_HISTORY_URL, json=fixture, status=200)

    expected = [
        {
            "date": m["created"],
            "detail_match": m["matchSimulation"],
            "victory": m["userWin"],
            "opponnent_name": m["adversaryPseudo"],
            "opponent_score": m["adversaryDeck"]["scoreDeck"],
            "opponent_id": m["adversaryId"],
            "user_score": m["userDeck"]["scoreDeck"],
            "userdeck": _expected_deck(m["userDeck"]["cardsEquipments"]),
            "opponentdeck": _expected_deck(m["adversaryDeck"]["cardsEquipments"]),
        }
        for m in fixture["data"]["matches"]
    ]

    assert client.match_history.get_match_history(5) == expected
