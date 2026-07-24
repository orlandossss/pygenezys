import responses

MISSIONS_URL = "https://app.genezys.xyz/api-prod-fantasy-game-service/missions/daily"


@responses.activate
def test_get_missions(client, load_fixture):
    fixture = load_fixture("missions_daily.json")
    responses.add(responses.GET, MISSIONS_URL, json=fixture, status=200)

    expected_rewards = [fixture["data"]["rewardType"], fixture["data"]["rewardQuantity"]]
    expected_missions = [
        {
            "title": m["title"],
            "reward_quantity": m["rewardQuantity"],
            "action_quantity": m["actionQuantity"],
            "reward_type": m["rewardType"],
        }
        for m in fixture["data"]["milestones"]
    ]

    all_rewards, missions_info = client.mission.get_missions()

    assert all_rewards == expected_rewards
    assert missions_info == expected_missions
