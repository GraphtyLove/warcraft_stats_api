from scrapper.battle_net.character_stats import get_character_stats
from scrapper.battle_net.character_spec import get_character_spec
from httpx import Client
from typing import Dict


def get_character_details(region: str, realm_slug: str, character_name: str, client: Client)-> Dict | None:
	stats = get_character_stats(region, realm_slug, character_name, client)
	spec = get_character_spec(region, realm_slug, character_name, client)
	if not stats or not spec:
		return None
	# Merge stats and spec dicts
	return {**stats, **spec}
