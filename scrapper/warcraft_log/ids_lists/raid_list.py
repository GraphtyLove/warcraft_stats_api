from typing import Dict

from custom_types.raid_types import RaidDifficulty, RaidName

raid_ids: Dict[RaidName, int] = {
	"Vault of the Incarnates": 31
}

raid_difficulty_ids: Dict[RaidDifficulty, int] = {
	"LFR": 1,
	"Normal": 3,
	"Heroic": 4,
	"Mythic": 5
}