from typing import Dict, List
from scrapper.warcraft_log.sanctum_of_domination import boss_ids
from scrapper.graph.query_handler import gql_query
from scrapper.graph.queries.encounter import ENCOUNTER_QUERY
from scrapper.battle_net.character_stats import get_character_stats
import re

player_classes_specs: Dict[str, List[str]] = {
    "DeathKnight": [
        "Unholy",
        "Frost",
        "Blood"
    ],
    "Druid": [
        "Restoration",
        "Balance",
        "Feral",
        "Guardian",
    ],
    "Hunter": [
        "BeastMastery",
        "Marksmanship",
        "Survival"
    ],
    "Mage": [
        "Arcane",
        "Fire",
        "Frost"
    ],
    "Monk": [
        "Brewmaster",
        "Mistweaver",
        "Windwalker"
    ],
    "Paladin": [
        "Holy",
        "Protection",
        "Retribution"
    ],
    "Priest": [
        "Discipline",
        "Holy",
        "Shadow"
    ],
    "Rogue": [
        "Assassination",
        "Subtlety",
        "Outlaw"
    ],
    "Shaman": [
        "Elemental",
        "Enhancement",
        "Restoration"
    ],
    "Warlock": [
        "Affliction",
        "Demonology",
        "Destruction"
    ],
    "Warrior": [
        "Arms",
        "Fury",
        "Protection"
    ],
    "DemonHunter": [
        "Havoc",
        "Vengeance"
    ]
}

covenant_ids: Dict[str, int] = {
    "Kyrian": 1,
    "Venthyr": 2,
    "Night Fae": 3,
    "Necrolord": 4
}

raid_ids: Dict[str, int] = {
    "Mythic+ Dungeons": 25,
    "Castle Nathria": 26,
    "Sanctum of Domination": 28
}

difficulty_ids: Dict[str, int] = {
    "LFR": 1,
    "Normal": 3,
    "Heroic": 4,
    "Mythic": 5
}

role_metrics: Dict[str, str] = {
    "dps": "dps",
    "heal": "hps"
}


def scrap_boss(raid: str, boss: str, player_class: str, player_spec: str, covenant: str, difficulty: str, role: str = "dps"):
    """
    Function that scrap warcraftlogs.com to get player names.

    :param raid: Int corresponding to the raid ID. ex: 28 (Sanctum of Domination)
    :param boss: Int corresponding to the boss ID. ex: 2423
    :param player_class: Player class. ex: Shaman
    :param player_spec: Player spec. ex: Elemental
    :param covenant_: Player covenant id. ex: 3 (fae)
    :param difficulty: Boss difficulty (nm, hm, MM). ex: 4 (hm)
    :return:
    """
    # Get IDs
    # raid_id = raid_ids[raid]
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

    for player in leader_board:
        # Filter players without asian chars.
        if re.match(r"([A-zÀ-ú]+)", player["name"]):
            print(f"Player: {player['name']}  {player['server']['name']}-{player['server']['region']}  => {int(player['amount'])}")
            server_slug = player['server']['name'].lower().replace(" ", "")
            get_character_stats(player['server']['regoin'], )