import os

import pytest

from pygenezys.client import GenezysClient

pytestmark = pytest.mark.skipif(
    not os.getenv("PYGENEZYS_LIVE_TOKEN"),
    reason="Set PYGENEZYS_LIVE_TOKEN to run live integration tests",
)


@pytest.fixture
def live_client():
    return GenezysClient(os.getenv("PYGENEZYS_LIVE_TOKEN"))


def test_get_username_live(live_client):
    assert isinstance(live_client.user.get_username(), str)


def test_get_user_id_live(live_client):
    assert isinstance(live_client.user.get_user_id(), str)


def test_get_gnz_live(live_client):
    assert isinstance(live_client.user.get_gnz(), (int, float))


def test_get_gems_live(live_client):
    assert isinstance(live_client.user.get_gems(), (int, float))


def test_user_get_all_info_live(live_client):
    assert isinstance(live_client.user.get_all_info(), dict)


def test_get_arena_info_live(live_client):
    name, category, attribut = live_client.arena.get_arena_info()
    assert isinstance(name, str)
    assert isinstance(category, list)
    assert isinstance(attribut, list)


def test_get_available_cups_id_live(live_client):
    assert isinstance(live_client.cup.get_available_cups_id(), list)


def test_get_available_cups_info_live(live_client):
    assert isinstance(live_client.cup.get_available_cups_info(), list)


def test_average_prices_live(live_client):
    limited, rare, epic, legendary = live_client.average_price.average_prices()
    assert isinstance(limited, (int, float))
    assert isinstance(rare, (int, float))
    assert isinstance(epic, (int, float))
    assert isinstance(legendary, (int, float))


def test_get_challenges_info_live(live_client):
    assert isinstance(live_client.challenges.get_challenges_info(), list)


def test_get_missions_live(live_client):
    all_rewards, missions_info = live_client.mission.get_missions()
    assert isinstance(all_rewards, list)
    assert isinstance(missions_info, list)


def test_division_leaderboard_live(live_client):
    own_info, players = live_client.ranking.division_leaderboard(5)
    assert isinstance(own_info, dict)
    assert isinstance(players, list)


def test_cup_leaderboard_live(live_client):
    cup_ids = live_client.cup.get_available_cups_id()
    if not cup_ids:
        pytest.skip("No active cups to test cup_leaderboard against")
    own_info, players = live_client.ranking.cup_leaderboard(cup_ids[0], 5)
    assert isinstance(own_info, dict)
    assert isinstance(players, list)


def test_get_daily_rewards_info_live(live_client):
    id_, reward_type, reward_quantity = live_client.rewards.get_daily_rewards_info()
    assert isinstance(id_, str)
    assert isinstance(reward_type, str)
    assert isinstance(reward_quantity, (int, float))


def test_get_missions_info_live(live_client):
    assert isinstance(live_client.rewards.get_missions_info(), list)


def test_get_transaction_history_live(live_client):
    assert isinstance(live_client.transaction_history.get_transaction_history(5), list)


def test_get_my_cards_live(live_client):
    assert isinstance(live_client.my_cards.get_my_cards(), dict)


def test_get_market_live(live_client):
    assert isinstance(live_client.market.get_market(), dict)
