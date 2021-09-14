from typing import Dict

from scrapper.battle_net.realms_list import get_realm_slug
from scrapper.warcraft_log.sanctum_of_domination import boss_ids
from scrapper.graph.query_handler import gql_query
from scrapper.graph.queries.encounter import ENCOUNTER_QUERY
from scrapper.battle_net.character_stats import get_character_stats
from scrapper.exceptions import CharacterNotFound
from scrapper.warcraft_log.wow_ids import covenant_ids, difficulty_ids
from scrapper.get_profils_url import get_character_profile_urls

reverted_covenant_id = {v: k for k, v in covenant_ids.items()}

role_metrics: Dict[str, str] = {
    "dps": "dps",
    "heal": "hps"
}


def format_amount(amount: int) -> str:
    formatted_with_coma = f"{amount:,}"
    formatted_with_space = formatted_with_coma.replace(',', ' ')
    return formatted_with_space


def scrap_boss(boss: str, player_class: str, player_spec: str, covenant: str, difficulty: str, progress_bar, role: str = "dps") -> dict:
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


    query_params = {
        "encounter_id": boss_id,
        "class_name": player_class,
        "spec_name": player_spec,
        "difficulty": difficulty_id,
        "metric":  role_metric,
    }

    if covenant_id:
        query_params["covenantID"] = covenant_id

    leader_board = gql_query(ENCOUNTER_QUERY, query_params)
    # Filter the json object to remove 2 lvl of abstraction.
    # Get the list of player with their data.
    leader_board = leader_board["worldData"]["encounter"]["characterRankings"]["rankings"]

    ranking_data = []

    for i, player in enumerate(leader_board):
        progress_bar.progress(i+1)
        if not player:
            print("Player NaN, Skiping...")
            continue
        if "server" not in player:
            print("No server, anonymous player.")
            continue
        # Filter players without asian chars.
        if player["server"]["region"] in ["EU", "US"]:
            print("PLAYER ", player)
            try:
                player_realm_slug = get_realm_slug(player['server']['name'])
                stats = get_character_stats(player['server']['region'], player_realm_slug, player['name'])
            except CharacterNotFound:
                continue
            except OSError:
                print('OS ERROR...')
                continue
            # Get profile URL for raiderIO + Bnet armory
            bnet_profile_url, raider_io_profile_url = get_character_profile_urls(
                player["server"]["region"],
                player_realm_slug,
                player["name"]
            )
            infos = {
                "name": player["name"],
                "covenant": reverted_covenant_id[player['covenantID']],
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

                },
                "profiles": {
                    "raider_io": raider_io_profile_url,
                    "bnet_armory": bnet_profile_url
                }
            }
            print(infos["name"], infos["server"])
            ranking_data.append(infos)
    return ranking_data
