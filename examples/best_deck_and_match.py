"""
Builds the best possible deck, plays a match, then re-checks the best deck
afterward (since health lost during the match can change which cards are
optimal). Runs this for both the division and every available cup, repeated
ITERATIONS times.

This performs real actions on your account: it overwrites your live deck(s)
and queues real matches, ITERATIONS times over. Set PYGENEZYS_TOKEN in a .env
file at the project root (or in your environment) to a fresh token before
running.
"""

import os

from dotenv import load_dotenv

from pygenezys import GenezysClient

DECK_SIZE = 5 

LEVEL_BONUS = {"talent": 50, "champion": 40, "star": 20}
LEVEL_PENALTY = {"talent": -10, "champion": -15, "star": -30}

CUP_BUILDERS_BY_HIGHEST_RARITY = {
    "Legendary": "build_deck_legendary_cup",
    "Epic": "build_deck_epic_cup",
    "Rare": "build_deck_rare_cup",
    "Limited": "build_deck_limited_cup",
}


def score_card(card, boosted_levels, boosted_characteristics):
    base_score = card["baseScore"]

    matching_value = sum(
        c["value"] for c in card["characteristics"] if c["name"] in boosted_characteristics
    )
    attribute_bonus = round(base_score * (matching_value * 5) / 100)

    level = card["level"]
    level_modifier = LEVEL_BONUS[level] if level in boosted_levels else LEVEL_PENALTY[level]
    level_bonus = round(base_score * level_modifier / 100)

    health_bonus = round(base_score * 15 / 100)
    performance_bonus = round(base_score * 20 / 100)

    arena_score = base_score + attribute_bonus + level_bonus + health_bonus + performance_bonus

    health_points = card["health"]["points"]
    if health_points < 40:
        health_multiplier = 0.40
    elif health_points < 70:
        health_multiplier = 0.70
    else:
        health_multiplier = 1.0

    return round(arena_score * health_multiplier)


def pick_best_deck(cards, boosted_levels, boosted_characteristics, deck_size=DECK_SIZE):
    scored = [(score_card(c, boosted_levels, boosted_characteristics), c) for c in cards]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [card for _, card in scored[:deck_size]]


def card_rarity(card):
    # Common cards omit "rarity" entirely and carry "type": "common" instead.
    return card.get("rarity", card.get("type"))


def build_function_for_cup(deck_resource, accepted_rarities):
    for rarity, method_name in CUP_BUILDERS_BY_HIGHEST_RARITY.items():
        if rarity in accepted_rarities:
            return getattr(deck_resource, method_name)
    return deck_resource.build_deck_commun_cup


def print_deck(label, cards):
    names = [f"{c['clientName']} ({c['level']}, hp={c['health']['points']})" for c in cards]
    print(f"{label}: {names}")


def optimize_and_play_division(client, boosted_levels, boosted_characteristics):
    print("=== Division ===")
    all_cards = client.my_cards.get_my_cards(max_results=100)["data"]["cardsList"]

    best_before = pick_best_deck(all_cards, boosted_levels, boosted_characteristics)
    print_deck("Best deck before match", best_before)
    print("Submit result:", client.deck.build_deck_division(best_before))

    print("Match result:", client.match.run_division_match())

    refreshed_cards = client.my_cards.get_my_cards(max_results=100)["data"]["cardsList"]
    best_after = pick_best_deck(refreshed_cards, boosted_levels, boosted_characteristics)
    print_deck("Best deck after match (health may have changed it)", best_after)
    print("Re-submit result:", client.deck.build_deck_division(best_after))


def optimize_and_play_cup(client, cup_id, accepted_rarities, boosted_levels, boosted_characteristics):
    print(f"=== Cup {cup_id} (accepts {accepted_rarities}) ===")
    all_cards = client.my_cards.get_my_cards(max_results=100)["data"]["cardsList"]
    eligible_cards = [c for c in all_cards if card_rarity(c) in accepted_rarities]
    build_deck = build_function_for_cup(client.deck, accepted_rarities)

    best_before = pick_best_deck(eligible_cards, boosted_levels, boosted_characteristics)
    print_deck("Best deck before match", best_before)
    print("Submit result:", build_deck(best_before))

    print("Match result:", client.match.run_cup_match(cup_id))

    refreshed_cards = client.my_cards.get_my_cards(max_results=100)["data"]["cardsList"]
    refreshed_eligible = [c for c in refreshed_cards if card_rarity(c) in accepted_rarities]
    best_after = pick_best_deck(refreshed_eligible, boosted_levels, boosted_characteristics)
    print_deck("Best deck after match (health may have changed it)", best_after)
    print("Re-submit result:", build_deck(best_after))


ITERATIONS = 10


def main():
    load_dotenv()
    client = GenezysClient(os.environ["PYGENEZYS_TOKEN"])

    for iteration in range(1, ITERATIONS + 1):
        print(f"\n########## Iteration {iteration}/{ITERATIONS} ##########")

        _, boosted_levels, boosted_characteristics = client.arena.get_arena_info()

        optimize_and_play_division(client, boosted_levels, boosted_characteristics)

        for cup in client.cup.get_available_cups_info():
            optimize_and_play_cup(
                client, cup["id"], cup["accepted_rarities"], boosted_levels, boosted_characteristics
            )


if __name__ == "__main__":
    main()
