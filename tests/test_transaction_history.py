import responses

TRANSACTIONS_URL = "https://app.genezys.xyz/api-prod-transaction-service/transactions"


@responses.activate
def test_get_transaction_history(client, load_fixture):
    fixture = load_fixture("transactions.json")
    responses.add(responses.GET, TRANSACTIONS_URL, json=fixture, status=200)

    expected = [
        {
            "date": t["created"],
            "type": t["origin"],
            "details": t["products"],
        }
        for t in fixture["data"]["transactionsList"]
    ]

    assert client.transaction_history.get_transaction_history(5) == expected
