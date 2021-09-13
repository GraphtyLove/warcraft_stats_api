from typing import Dict, List, Optional


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

covenant_ids: Dict[str, Optional[int]] = {
    "All": 0,
    "Kyrian": 1,
    "Venthyr": 2,
    "NightFae": 3,
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
