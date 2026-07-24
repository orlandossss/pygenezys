import responses

DAILY_REWARDS_URL = "https://app.genezys.xyz/api-prod-fantasy-game-service/daily-rewards/current"
MISSIONS_URL = "https://app.genezys.xyz/api-prod-fantasy-game-service/missions/daily"


@responses.activate
def test_get_daily_rewards_info(client, load_fixture):
    fixture = load_fixture("daily_rewards_current.json")
    responses.add(responses.GET, DAILY_REWARDS_URL, json=fixture, status=200)

    id_, reward_type, reward_quantity = client.rewards.get_daily_rewards_info()

    assert id_ == fixture["data"]["id"]
    assert reward_type == fixture["data"]["rewardType"]
    assert reward_quantity == fixture["data"]["rewardQuantity"]


@responses.activate
def test_get_missions_info(client, load_fixture):
    fixture = load_fixture("missions_daily.json")
    responses.add(responses.GET, MISSIONS_URL, json=fixture, status=200)

    expected = [
        {
            "title": m["title"],
            "reward_quantity": m["rewardQuantity"],
            "action_quantity": m["actionQuantity"],
            "reward_type": m["rewardType"],
        }
        for m in fixture["data"]["milestones"]
    ]
    expected.append({
        "title": "Finir toutes les misions",
        "reward_quantity": fixture["data"]["rewardQuantity"],
        "reward_type": fixture["data"]["rewardType"],
    })

    assert client.rewards.get_missions_info() == expected
