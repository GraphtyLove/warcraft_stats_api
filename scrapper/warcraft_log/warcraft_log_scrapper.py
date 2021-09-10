from typing import Dict
from scrapper.warcraft_log.sanctum_of_domination import boss_ids
from scrapper.graph.query_handler import gql_query
from scrapper.graph.queries.encounter import ENCOUNTER_QUERY
from scrapper.battle_net.character_stats import get_character_stats
from scrapper.exceptions import CharacterNotFound
from scrapper.warcraft_log.wow_ids import covenant_ids, difficulty_ids


role_metrics: Dict[str, str] = {
    "dps": "dps",
    "heal": "hps"
}


def format_amount(amount: int) -> str:
    formatted_with_coma = f"{amount:,}"
    formatted_with_space = formatted_with_coma.replace(',', ' ')
    return formatted_with_space


def scrap_boss(boss: str, player_class: str, player_spec: str, covenant: str, difficulty: str, role: str = "dps") -> dict:
    """
    Function that scrap warcraftlogs.com to get player names.

    :param boss: Int corresponding to the boss ID. ex: 2423
    :param player_class: Player class. ex: Shaman
    :param player_spec: Player spec. ex: Elemental
    :param covenant_: Player covenant id. ex: 3 (fae)
    :param difficulty: Boss difficulty (nm, hm, MM). ex: 4 (hm)
    :param role: dps or heal
    :return:
    """
    # Get IDs
    boss_id = boss_ids[boss]
    covenant_id = covenant_ids[covenant]
    difficulty_id = difficulty_ids[difficulty]
    role_metric = role_metrics[role]

    leader_board = gql_query(ENCOUNTER_QUERY, {
        "encounter_id": boss_id,
        "class_name": player_class,
        "spec_name": player_spec,
        "difficulty": difficulty_id,
        "metric":  role_metric,
        "covenantID": covenant_id
    })
    # Filter the json object to remove 2 lvl of abstraction.
    # Get the list of player with their data.
    leader_board = leader_board["worldData"]["encounter"]["characterRankings"]["rankings"]

    ranking_data = []

    for i, player in enumerate(leader_board):
        # Filter players without asian chars.
        if player["server"]["region"] in ["EU", "US"]:
            try:
                stats = get_character_stats(player['server']['region'], player['server']['name'], player['name'])
            except CharacterNotFound:
                continue
            except OSError:
                print('OS ERROR...')
                continue

            infos = {
                "name": player["name"],
                "rank": i,
                "server": f"{player['server']['name']}-{player['server']['region'].lower()}",
                "amount": format_amount(int(player["amount"])),
                "stats": {
                    "mastery": round(stats["mastery"]["value"], 2),
                    "haste": round(stats["spell_haste"]["value"], 2),
                    "crit": round(stats["spell_crit"]["value"], 2),
                    "haste": round(stats["spell_haste"]["value"], 2),
                    "versatility": round(stats["versatility"], 2),
                    "intellect": round(stats["intellect"]["effective"], 2),
                    "agility": round(stats["agility"]["effective"], 2),
                    "strength": round(stats["strength"]["effective"], 2),

                }
            }
            print(infos["name"], infos["server"])
            ranking_data.append(infos)
    return ranking_data
