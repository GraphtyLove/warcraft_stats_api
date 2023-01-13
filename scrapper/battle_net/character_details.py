from scrapper.battle_net.character_stats import get_character_stats
from scrapper.battle_net.character_spec import get_character_spec
from httpx import Client


def get_character_details(region: str, realm_slug: str, character_name: str, client: Client):
	stats = get_character_stats(region, realm_slug, character_name, client)
	spec = get_character_spec(region, realm_slug, character_name, client)
	# Merge stats and spec dicts
	return {**stats, **spec}
