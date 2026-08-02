# pygenezys

Une librarie Python non officiel pour [Genezys](https://app.genezys.xyz).

> **Avertissement** : il s'agit d'une librarie non officiel, développé par la communauté. Il n'est pas
> affilié, approuvé ou supporté par Genezys. Il utilise des endpoints API
> internes non documentés, qui peuvent changer ou cesser de fonctionner sans
> préavis. L'utilisation de ces endpoints peut être soumise aux Conditions
> d'utilisation de Genezys — utilisez-le à vos propres risques.

## Installation

```
pip install pygenezys
```

## Obtenir un token

`pygenezys` ne se connecte pas en votre nom — vous fournissez votre propre
token de session, le même que celui utilisé par le site web :

1. Connectez-vous sur [app.genezys.xyz](https://app.genezys.xyz) dans votre navigateur.
2. Ouvrez les outils de développement de votre navigateur (F12) ou faites un clic droit et cliquez sur 'inspecter' <img width="1871" height="860" alt="inspected" src="https://github.com/user-attachments/assets/cfb1a386-a34e-46f9-bf93-3ec9cd8f7806" />

3. Allez dans l'onglet Réseau (Network). <img width="1885" height="821" alt="2" src="https://github.com/user-attachments/assets/0b03177a-32f9-4ef3-916d-b6679e837572" />

4. Rechargez la page et trouvez une requête vers `app.genezys.xyz`.<img width="1917" height="862" alt="5" src="https://github.com/user-attachments/assets/751245f6-52e9-44cc-b96c-62db6526d2a3" />

5. Copiez la valeur de l'en-tête de requête `Authorization` — c'est votre token.<img width="1873" height="755" alt="6" src="https://github.com/user-attachments/assets/c01b1cb6-31c0-4a31-8579-c2f278b3f161" />


Ce token a une durée de vie limitée (environ une heure). Une fois expiré, répétez les
étapes ci-dessus pour en obtenir un nouveau et passez-le à `set_token()` (voir ci-dessous)
au lieu de créer un nouveau client.

## Démarrage rapide

```python
from pygenezys import GenezysClient

client = GenezysClient("votre-token-ici")

print(client.user.get_username())
print(client.user.get_gnz())
print(client.cup.get_available_cups_id())
```

Lorsque votre token expire, remplacez-le par un nouveau sur le même client au lieu de
le réinstancier :

```python
client.set_token("votre-nouveau-token-ici")
```

## Installation pour le développement

Pour installer pygenezys en mode développement (éditable) :

```bash
git clone <repository-url>
cd pygenezys
pip install -e .
```

Pour installer avec les dépendances de développement :

```bash
pip install -e .[dev]
```

## Exemples

Le répertoire `examples/` contient des scripts d'exemple démontrant l'utilisation de pygenezys.

### Exécuter les exemples

Les exemples nécessitent un token Genezys valide. Créez un fichier `.env` à la racine du projet :

```bash
# .env
PYGENEZYS_TOKEN=votre-token-ici
```

Installez les dépendances des exemples :

```bash
pip install -e .[examples]
```

Ensuite exécutez n'importe quel exemple :

```bash
python examples/best_deck_and_match.py
```

### `best_deck_and_match.py`

Cet exemple automatise l'optimisation de deck et le jeu de matchs :

- Récupère les informations de l'arène actuelle (niveaux et caractéristiques boostés)
- Calcule les meilleurs decks possibles pour la division et toutes les coupes disponibles
- Soumet ces decks à votre compte
- Joue automatiquement des matchs
- Re-calcule et soumet les meilleurs decks après chaque match (car les points de vie peuvent changer)

**⚠️ Attention** : Ce script effectue des actions réelles sur votre compte :
- Il écrase vos decks en direct
- Il met en file d'attente et joue de vrais matchs
- Il s'exécute `ITERATIONS` fois (défini à 10 par défaut)

Utilisez-le avec précaution et assurez-vous de comprendre ce qu'il fait avant de l'exécuter.

## Ressources disponibles

Chaque ressource est organisée par namespace sur le client et reflète une zone fonctionnelle de Genezys.
Les méthodes marquées **⚠ modifie** changent l'état réel de votre compte (deck ou file
d'attente de match) au lieu de simplement lire les données — utilisez-les délibérément.

### `client.user`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_username()` | — | `str` — le nom d'affichage du compte (pseudo). |
| `get_gnz()` | — | `int` — solde de tokens GNZ. |
| `get_gems()` | — | `int` — solde de gemmes. |
| `get_activity_points()` | — | `int` — points d'activité gagnés cette période, en attente de réclamation. |
| `get_airdrop()` | — | `int` — tokens en attente de réclamation depuis l'airdrop. |
| `get_user_id()` | — | `str` — ID utilisateur interne. |
| `get_all_info()` | — | `dict` — réponse brute complète de `/users/connected`. |

### `client.arena`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_arena_info()` | — | `(name, boosted_levels, boosted_characteristics)` — `name: str` est le titre de l'arène actuelle ; `boosted_levels: list[str]` sont les niveaux de cartes (par ex. `"talent"`, `"champion"`, `"star"`) notés favorablement cette période ; `boosted_characteristics: list[str]` sont les noms de caractéristiques (par ex. `"Power"`, `"Technique"`) notées favorablement cette période. |

### `client.average_price`

| Méthode | Paramètres | Retour |
|---|---|---|
| `average_prices()` | — | `(limited_price, rare_price, epic_price, legendary_price)` — chacun est un `float`, le prix de vente moyen sur le marché pour cette rareté. |

### `client.challenges`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_challenges_info()` | — | `list[dict]` — une entrée par défi actif : `{name, athlete, total_entries, start_date, end_date}`. |

### `client.cup`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_available_cups_id()` | — | `list[str]` — IDs des coupes actuellement disponibles. |
| `get_available_cups_info()` | — | `list[dict]` — une entrée par coupe : `{id: str, accepted_rarities: list[str]}` (par ex. `["common", "Limited"]`). |
| `get_all_info()` | — | `dict` — réponse brute complète de `/cups`. |

### `client.deck`

Chaque méthode `build_deck_*` prend les mêmes paramètres et retourne la même structure ;
elles diffèrent uniquement par la ligue/coupe à laquelle elles soumettent. **⚠ modifie** —
chaque appel écrase votre deck en direct pour cette ligue/coupe.

| Méthode | Paramètres | Retour |
|---|---|---|
| `build_deck_division(card_info)` | `card_info: list[dict]` — cartes à aligner, telles que retournées par `client.my_cards.get_my_cards()` (chacune nécessite au moins `id` et `collectionId`, plus un `equipmentId` optionnel) | `str` — le message de réponse de l'API. |
| `build_deck_commun_cup(card_info)` | identique à ci-dessus | `str` |
| `build_deck_limited_cup(card_info)` | identique à ci-dessus | `str` |
| `build_deck_rare_cup(card_info)` | identique à ci-dessus | `str` |
| `build_deck_epic_cup(card_info)` | identique à ci-dessus | `str` |
| `build_deck_legendary_cup(card_info)` | identique à ci-dessus | `str` |
| `get_current_decks()` | — | `dict[str, list[dict]]` — deck actuel par emplacement, indexé par nom d'emplacement (`"division"`, `"cup_common"`, `"cup_limited"`, `"cup_rare"`, `"cup_epic"`, `"cup_legendary"` ; les emplacements non reconnus sont indexés par leur hash brut). Chaque valeur est la liste `cardsSummary` de ce deck. |

### `client.items`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_items_info(item_type=None)` | `item_type: str \| None` — filtrer sur `"consumable"` ou `"equipment"` ; `None` retourne les deux. Lève `ValueError` pour toute autre valeur. | `list[dict]` — une entrée par objet : `{id, type, title, quantity, in_nb_deck_usage, health_points, boosted_characteristics}`. `id` est la valeur à passer comme `equipmentId` lors de la construction d'un deck (voir `client.deck`). `health_points` est `None` pour les objets qui ne restaurent pas de santé (équipement). `boosted_characteristics: list[dict]` est `{name, boost_percentage}` par caractéristique boostée (vide pour les objets sans boost). |
| `get_all_info()` | — | `dict` — réponse brute complète de `/items`. |

### `client.match`

**⚠ modifie** — les deux méthodes mettent en file d'attente/jouent un vrai match sur votre compte.

| Méthode | Paramètres | Retour |
|---|---|---|
| `run_division_match()` | — | `dict` — réponse API brute (vide en cas de succès). |
| `run_cup_match(cup_id)` | `cup_id: str` — un ID de coupe de `client.cup.get_available_cups_id()` | `dict` — réponse API brute (vide en cas de succès). |

### `client.match_history`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_match_history(numberof_matches=10)` | `numberof_matches: int` — nombre de matchs passés à récupérer | `list[dict]` — une entrée par match : `{date, detail_match, victory: bool, opponnent_name, opponent_score, opponent_id, user_score, userdeck, opponentdeck}`. `userdeck`/`opponentdeck` sont chacun `list[dict]` de `{card_name, score, health}`. |

### `client.mission`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_missions()` | — | `(all_missions_rewards, missions_info)` — `all_missions_rewards: [reward_type, reward_quantity]` pour avoir terminé toutes les missions quotidiennes ; `missions_info: list[dict]` est une entrée par mission : `{title, reward_quantity, action_quantity, reward_type}`. |

### `client.my_cards`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_my_cards(order='desc', sortBy='baseScore', max_results=20)` | `order: str`, `sortBy: str`, `max_results: int` | `dict` — réponse brute ; les cartes sont dans `["data"]["cardsList"]`. Chaque carte a `rarity` (cartes de niveau de rareté) ou `type: "common"` (communes, pas de clé `rarity`), plus `level`, `health.points`, `characteristics`, `baseScore`, etc. |

### `client.market`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_market(order='desc', sortBy='date', max_results=20)` | `order: str`, `sortBy: str`, `max_results: int` | `dict` — réponse brute ; les annonces sont dans `["data"]["listings"]`, avec `["data"]["nextKey"]` pour la pagination. |

### `client.ranking`

| Méthode | Paramètres | Retour |
|---|---|---|
| `cup_leaderboard(cup_id, max_results=10)` | `cup_id: str`, `max_results: int` | `(own_info, players)` — `own_info: dict` est `{score, matchplayed, position}` pour l'utilisateur actuel ; `players: list[dict]` sont les meilleures entrées, chacune `{score, name, userId, matchplayed, position}`. |
| `division_leaderboard(max_results)` | `max_results: int` | `(own_info, players)` — `own_info: dict` est `{score, matchplayed, position, division_rank}` ; `players` a la même structure que ci-dessus. |

### `client.rewards`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_daily_rewards_info()` | — | `(id, reward_type, reward_quantity)` — l'ID, le type et la quantité de la récompense quotidienne actuelle. |
| `get_missions_info()` | — | `list[dict]` — une entrée par mission quotidienne (`{title, reward_quantity, action_quantity, reward_type}`), plus une entrée finale pour le bonus "terminer toutes les missions" (`{title, reward_quantity, reward_type}`, pas de `action_quantity`). |

### `client.transaction_history`

| Méthode | Paramètres | Retour |
|---|---|---|
| `get_transaction_history(numberof_matches=10)` | `numberof_matches: int` — nombre de transactions passées à récupérer | `list[dict]` — une entrée par transaction : `{date, type, details}`. |

## Formats des réponses

Vous pouvez trouver tous les exemples de réponses JSON et leurs champs attendus dans pygenezys/tests/fixtures.

## Licence

MIT

---

# English Version

# pygenezys

An unofficial Python client for [Genezys](https://app.genezys.xyz).

> **Disclaimer**: this is an unofficial, community-built client. It is not
> affiliated with, endorsed by, or supported by Genezys. It talks to
> undocumented, internal API endpoints, which may change or break without
> notice. Use of these endpoints may be subject to Genezys's Terms of
> Service — use at your own risk.

## Installation

```
pip install pygenezys
```

## Getting a token

`pygenezys` does not log in on your behalf — you provide your own session
token, the same one the website itself uses:

1. Log into [app.genezys.xyz](https://app.genezys.xyz) in your browser.
2. Open your browser's developer tools (F12) or right-click and click on 'inspect' <img width="1871" height="860" alt="inspected" src="https://github.com/user-attachments/assets/cfb1a386-a34e-46f9-bf93-3ec9cd8f7806" />

3. Go to the Network tab. <img width="1885" height="821" alt="2" src="https://github.com/user-attachments/assets/0b03177a-32f9-4ef3-916d-b6679e837572" />

4. Reload the page and find any request to `app.genezys.xyz`.<img width="1917" height="862" alt="5" src="https://github.com/user-attachments/assets/751245f6-52e9-44cc-b96c-62db6526d2a3" />

5. Copy the value of the `Authorization` request header — that's your token.<img width="1873" height="755" alt="6" src="https://github.com/user-attachments/assets/c01b1cb6-31c0-4a31-8579-c2f278b3f161" />


This token is short-lived (roughly one hour). Once it expires, repeat the
steps above to get a new one and pass it to `set_token()` (see below)
instead of creating a new client.

## Quickstart

```python
from pygenezys import GenezysClient

client = GenezysClient("your-token-here")

print(client.user.get_username())
print(client.user.get_gnz())
print(client.cup.get_available_cups_id())
```

When your token expires, swap in a fresh one on the same client instead of
re-instantiating:

```python
client.set_token("your-new-token-here")
```

## Development Installation

To install pygenezys in development (editable) mode:

```bash
git clone <repository-url>
cd pygenezys
pip install -e .
```

To install with development dependencies:

```bash
pip install -e .[dev]
```

## Examples

The `examples/` directory contains example scripts demonstrating pygenezys usage.

### Running Examples

Examples require a valid Genezys token. Create a `.env` file at the project root:

```bash
# .env
PYGENEZYS_TOKEN=your-token-here
```

Install example dependencies:

```bash
pip install -e .[examples]
```

Then run any example:

```bash
python examples/best_deck_and_match.py
```

### `best_deck_and_match.py`

This example automates deck optimization and match playing:

- Fetches current arena information (boosted levels and characteristics)
- Calculates the best possible decks for division and all available cups
- Submits these decks to your account
- Automatically plays matches
- Re-calculates and submits the best decks after each match (as health points may change)

**⚠️ Warning**: This script performs real actions on your account:
- It overwrites your live decks
- It queues and plays real matches
- It runs `ITERATIONS` times (set to 10 by default)

Use it carefully and make sure you understand what it does before running it.

## Available resources

Each resource is namespaced on the client and mirrors a Genezys feature area.
Methods marked **⚠ mutates** change your live account state (deck or match
queue) instead of just reading data — use them deliberately.

### `client.user`

| Method | Takes | Returns |
|---|---|---|
| `get_username()` | — | `str` — the account's display name (pseudo). |
| `get_gnz()` | — | `int` — GNZ token balance. |
| `get_gems()` | — | `int` — gem balance. |
| `get_activity_points()` | — | `int` — activity points earned this period, pending claim. |
| `get_airdrop()` | — | `int` — tokens pending claim from the airdrop. |
| `get_user_id()` | — | `str` — internal user ID. |
| `get_all_info()` | — | `dict` — full raw `/users/connected` response. |

### `client.arena`

| Method | Takes | Returns |
|---|---|---|
| `get_arena_info()` | — | `(name, boosted_levels, boosted_characteristics)` — `name: str` is the current arena's title; `boosted_levels: list[str]` are the card levels (e.g. `"talent"`, `"champion"`, `"star"`) scored favorably this period; `boosted_characteristics: list[str]` are the characteristic names (e.g. `"Power"`, `"Technique"`) scored favorably this period. |

### `client.average_price`

| Method | Takes | Returns |
|---|---|---|
| `average_prices()` | — | `(limited_price, rare_price, epic_price, legendary_price)` — each a `float`, the average marketplace sale price for that rarity. |

### `client.challenges`

| Method | Takes | Returns |
|---|---|---|
| `get_challenges_info()` | — | `list[dict]` — one entry per active challenge: `{name, athlete, total_entries, start_date, end_date}`. |

### `client.cup`

| Method | Takes | Returns |
|---|---|---|
| `get_available_cups_id()` | — | `list[str]` — IDs of currently available cups. |
| `get_available_cups_info()` | — | `list[dict]` — one entry per cup: `{id: str, accepted_rarities: list[str]}` (e.g. `["common", "Limited"]`). |
| `get_all_info()` | — | `dict` — full raw `/cups` response. |

### `client.deck`

Every `build_deck_*` method takes the same input and returns the same shape;
they differ only in which league/cup tier they submit to. **⚠ mutates** —
each call overwrites your live deck for that league/cup.

| Method | Takes | Returns |
|---|---|---|
| `build_deck_division(card_info)` | `card_info: list[dict]` — cards to field, as returned by `client.my_cards.get_my_cards()` (each needs at least `id` and `collectionId`, plus an optional `equipmentId`) | `str` — the API's response message. |
| `build_deck_commun_cup(card_info)` | same as above | `str` |
| `build_deck_limited_cup(card_info)` | same as above | `str` |
| `build_deck_rare_cup(card_info)` | same as above | `str` |
| `build_deck_epic_cup(card_info)` | same as above | `str` |
| `build_deck_legendary_cup(card_info)` | same as above | `str` |
| `get_current_decks()` | — | `dict[str, list[dict]]` — current deck per slot, keyed by slot name (`"division"`, `"cup_common"`, `"cup_limited"`, `"cup_rare"`, `"cup_epic"`, `"cup_legendary"`; unrecognized slots are keyed by their raw hash). Each value is that deck's `cardsSummary` list. |

### `client.items`

| Method | Takes | Returns |
|---|---|---|
| `get_items_info(item_type=None)` | `item_type: str \| None` — filter to `"consumable"` or `"equipment"`; `None` returns both. Raises `ValueError` on any other value. | `list[dict]` — one entry per item: `{id, type, title, quantity, in_nb_deck_usage, health_points, boosted_characteristics}`. `id` is the value to pass as `equipmentId` when building a deck (see `client.deck`). `health_points` is `None` for items that don't restore health (equipment). `boosted_characteristics: list[dict]` is `{name, boost_percentage}` per boosted characteristic (empty for items with no boosts). |
| `get_all_info()` | — | `dict` — full raw `/items` response. |

### `client.match`

**⚠ mutates** — both methods queue/play a real match on your account.

| Method | Takes | Returns |
|---|---|---|
| `run_division_match()` | — | `dict` — raw API response (empty on success). |
| `run_cup_match(cup_id)` | `cup_id: str` — a cup ID from `client.cup.get_available_cups_id()` | `dict` — raw API response (empty on success). |

### `client.match_history`

| Method | Takes | Returns |
|---|---|---|
| `get_match_history(numberof_matches=10)` | `numberof_matches: int` — how many past matches to fetch | `list[dict]` — one entry per match: `{date, detail_match, victory: bool, opponnent_name, opponent_score, opponent_id, user_score, userdeck, opponentdeck}`. `userdeck`/`opponentdeck` are each `list[dict]` of `{card_name, score, health}`. |

### `client.mission`

| Method | Takes | Returns |
|---|---|---|
| `get_missions()` | — | `(all_missions_rewards, missions_info)` — `all_missions_rewards: [reward_type, reward_quantity]` for clearing every daily mission; `missions_info: list[dict]` is one entry per mission: `{title, reward_quantity, action_quantity, reward_type}`. |

### `client.my_cards`

| Method | Takes | Returns |
|---|---|---|
| `get_my_cards(order='desc', sortBy='baseScore', max_results=20)` | `order: str`, `sortBy: str`, `max_results: int` | `dict` — raw response; cards are at `["data"]["cardsList"]`. Each card has `rarity` (rarity-tier cards) or `type: "common"` (commons, no `rarity` key), plus `level`, `health.points`, `characteristics`, `baseScore`, etc. |

### `client.market`

| Method | Takes | Returns |
|---|---|---|
| `get_market(order='desc', sortBy='date', max_results=20)` | `order: str`, `sortBy: str`, `max_results: int` | `dict` — raw response; listings are at `["data"]["listings"]`, with `["data"]["nextKey"]` for pagination. |

### `client.ranking`

| Method | Takes | Returns |
|---|---|---|
| `cup_leaderboard(cup_id, max_results=10)` | `cup_id: str`, `max_results: int` | `(own_info, players)` — `own_info: dict` is `{score, matchplayed, position}` for the current user; `players: list[dict]` is the top entries, each `{score, name, userId, matchplayed, position}`. |
| `division_leaderboard(max_results)` | `max_results: int` | `(own_info, players)` — `own_info: dict` is `{score, matchplayed, position, division_rank}`; `players` has the same shape as above. |

### `client.rewards`

| Method | Takes | Returns |
|---|---|---|
| `get_daily_rewards_info()` | — | `(id, reward_type, reward_quantity)` — the current daily reward's ID, type, and quantity. |
| `get_missions_info()` | — | `list[dict]` — one entry per daily mission (`{title, reward_quantity, action_quantity, reward_type}`), plus a trailing entry for the "finish every mission" bonus (`{title, reward_quantity, reward_type}`, no `action_quantity`). |

### `client.transaction_history`

| Method | Takes | Returns |
|---|---|---|
| `get_transaction_history(numberof_matches=10)` | `numberof_matches: int` — how many past transactions to fetch | `list[dict]` — one entry per transaction: `{date, type, details}`. |

## Forms of answers

You can find every exemple of every json answers and their expected field in pygenezys/tests
/fixtures.

## License

MIT
