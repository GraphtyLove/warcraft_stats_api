from typing import Dict

from custom_types.raid_types import RaidName, BossName

boss_ids: Dict[RaidName, Dict[BossName, int]] = {

    "Castle Nathria": {
        "Shriekwing": 2398,
        "Huntsman Altimor": 2418,
        "Hungering Destroyer": 2383,
        "Sun King's Salvation": 2402,
        "Artificer Xy'mox": 2405,
        "Lady Inerva Darkvein": 2406,
        "The Council of Blood": 2412,
        "Sludgefist": 2399,
        "Stone Legion Generals": 2417,
        "Sire Denathrius": 2407,
    },

    "Sanctum Of Domination": {
        "The Tarragrue": 2423,
        "The Eye of the Jailer": 2433,
        "The Nine": 2429,
        "Remnant of Ner'zhul": 2432,
        "Soulrender Dormazain": 2434,
        "Painsmith Raznal": 2430,
        "Guardian of the First Ones": 2436,
        "Fatescribe Roh-Kalo": 2431,
        "Kel'Thuzad": 2422,
        "Sylvanas Windrunner": 2435
    }
}