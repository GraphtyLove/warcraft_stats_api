from typing import Dict

from custom_types.raid_types import RaidName, BossName

boss_ids: Dict[RaidName, Dict[BossName, int]] = {
   "Vault of the Incarnates": {
        "Eranog": 2587,
        "Terros": 2639,
        "The Pirmal Council": 2590,
        "Sennerath": 2592,
        "Dathea": 2635,
        "Kurog": 2605,
        "Diurna": 2614,
        "Raszageth": 2607
    }
}