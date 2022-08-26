from typing import Dict, List

from custom_types.class_and_specs import ClassName, SpecName
from custom_types.player_role_types import PlayerRole
from custom_types.raid_types import BossName, RaidDifficulty, RaidName
from custom_types.shadowland_types import CovenantName
from scrapper.battle_net.realms_list import get_realm_slug
from scrapper.warcraft_log.ids_lists.boss_list import boss_ids
from scrapper.graph.query_handler import gql_query
from scrapper.graph.queries.encounter import ENCOUNTER_QUERY
from scrapper.battle_net.character_stats import get_character_stats
from scrapper.exceptions import CharacterNotFound
from scrapper.get_profils_url import get_character_profile_urls
from scrapper.warcraft_log.ids_lists.raid_list import raid_difficulty_ids
from scrapper.warcraft_log.ids_lists.shadowland_specific import covenant_ids

reverted_covenant_id = {v: k for k, v in covenant_ids.items()}

role_metrics: Dict[PlayerRole, str] = {
    "dps": "dps",
    "heal": "hps",
    "tank": "dps"
}


def format_amount(amount: int) -> str:
    formatted_with_coma = f"{amount:,}"
    formatted_with_space = formatted_with_coma.replace(',', ' ')
    return formatted_with_space


def get_characters_list(leader_board: list):
    player_names = []
    for i, player in enumerate(leader_board):
        if not player:
            print("Player NaN, Skiping...")
            continue
        if "server" not in player:
            print("No server, anonymous player.")
            continue
        # Filter players without asian chars.
        if player["server"]["region"] in ["EU", "US"]:
            player["rank"] = i + 1
            player_names.append(player)
    return player_names


def scrap_boss(
        raid_name: RaidName,
        boss: BossName,
        player_class: ClassName,
        player_spec: SpecName,
        covenant: CovenantName,
        difficulty: RaidDifficulty,
        role: PlayerRole = "dps",
        result_per_page: int = 10,
        pagination: int = 2
) -> List[Dict] | str:
    """
    Function that scrap warcraftlogs.com to get player names.

    :param boss: Int corresponding to the boss ID. ex: 2423
    :param player_class: Player class. ex: Shaman
    :param player_spec: Player spec. ex: Elemental
    :param covenant: Player covenant id. ex: 3 (fae)
    :param difficulty: Boss difficulty (nm, hm, MM). ex: 4 (hm)
    :param role: dps or heal.
    :param result_per_page: Number of page per result
    :param pagination: page number.
    :return:
    """
    # Get IDs
    try:
        boss_id = boss_ids[raid_name][boss]
        covenant_id = covenant_ids[covenant]
        difficulty_id = raid_difficulty_ids[difficulty]
        role_metric = role_metrics[role]
    except KeyError as ex:
        print(ex)
        return f"Param: {ex} not valid"

    query_params = {
        "encounter_id": boss_id,
        "class_name": player_class,
        "spec_name": player_spec,
        "difficulty": difficulty_id,
        "metric": role_metric,
    }

    if covenant_id:
        query_params["covenantID"] = covenant_id

    leader_board = gql_query(ENCOUNTER_QUERY, query_params)
    # Filter the json object to remove 2 lvl of abstraction.
    # Get the list of player with their data.
    leader_board = leader_board["worldData"]["encounter"]["characterRankings"]["rankings"]

    ranking_data = []

    result_range_start = ((pagination - 1) * result_per_page)
    result_range_end = pagination * result_per_page

    # Filter players without asian chars and remove anonymous players
    characters_list = get_characters_list(leader_board)
    if not characters_list:
        return "no character found."

    for i in range(result_range_start, result_range_end):
        print(i, result_range_start, result_range_end)
        player = characters_list[i]
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
            "rank": player["rank"],
            "server": f"{player['server']['name']}-{player['server']['region'].lower()}",
            "amount": format_amount(int(player["amount"])),
            "stats": stats,
            "profiles": {
                "raider_io": raider_io_profile_url,
                "bnet_armory": bnet_profile_url
            }
        }
        print(infos["name"], infos["server"])
        ranking_data.append(infos)
    return ranking_data
