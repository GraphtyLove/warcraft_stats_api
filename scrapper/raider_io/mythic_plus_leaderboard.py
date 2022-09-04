import asyncio
from math import ceil
from typing import Dict, List

from httpx import AsyncClient, Client

from custom_types.class_and_specs import ClassName, SpecName
from custom_types.region import Region
from scrapper.battle_net.character_details import get_character_details
from scrapper.battle_net.character_stats import get_character_stats
from scrapper.exceptions import ApiDataError
from scrapper.get_profils_url import get_character_profile_urls
from scrapper.http_request import get_request_async


def format_leaderboard_request_url(
		class_name: ClassName, spec_name: SpecName, region: Region = "world", season: str = "season-sl-4", page: int = 0
) -> str:
	return f"https://raider.io/api/mythic-plus/rankings/specs?" \
	       f"region={region}" \
	       f"&season={season}" \
	       f"&class={class_name.lower()}" \
	       f"&spec={spec_name.lower()}" \
	       f"&page={page}"


def format_leaderboard_page_results(leader_board_result: Dict) -> List[Dict]:
	character_list = leader_board_result.get("rankings", {}).get("rankedCharacters", [])
	formatted_characters = []

	if not character_list:
		raise ApiDataError("RaiderIO API: rankings.rankedCharacters not found in json")

	for character in character_list:
		character_data = character.get("character", {})
		realm_data = character_data.get("realm")

		covenant_icon_slug = character_data.get("covenant", {}).get("icon")
		realm_region = character_data.get("region").get("slug")
		bnet_profile_url, raider_io_profile_url, warcraft_log_url = get_character_profile_urls(
			realm_region, realm_data.get("slug"), character_data.get("name")
		)
		formatted_characters.append({
			"name": character_data.get("name"),
			"region": realm_region,
			"realm": realm_data.get("name"),
			"realm_slug": realm_data.get("slug"),
			"profiles": {
				"raider_io": raider_io_profile_url,
				"bnet_armory": bnet_profile_url,
				"warcraft_log": warcraft_log_url
			},
			"rank": character.get("rank"),
			"score": character.get("score"),
			"score_color": character.get("scoreColor"),
			"covenant": character_data.get("covenant", {}).get("name"),
			"covenant_icon_url": f"https://cdnassets.raider.io/images/wow/icons/large/{covenant_icon_slug}.jpg",
			"faction": character_data.get("faction"),
			"is_connected": realm_data.get("isConnected")
		})
	return formatted_characters


async def get_leaderboard_for_class_and_spec(
		class_name: ClassName, spec_name: SpecName, region: Region = "world", season: str = "season-sl-4",
		max_characters: int = 60
) -> List[Dict]:
	# RaiderIo API returns 20 players per page
	player_per_page = 20
	number_of_pages = ceil(max_characters / player_per_page)

	leaderboard = []
	tasks = []
	async with AsyncClient(timeout=5000) as client:
		for page_number in range(number_of_pages):
			page_url = format_leaderboard_request_url(class_name, spec_name, region, season, page_number)
			tasks.append(asyncio.create_task(
				get_request_async(url=page_url, client=client)
			))

		pages_data = await asyncio.gather(*tasks)

	for page_data in pages_data:
		leaderboard.extend(format_leaderboard_page_results(page_data))

	leaderboard_with_stats = await add_character_stats_to_leaderboard(leaderboard)
	return leaderboard_with_stats


async def add_character_stats_to_leaderboard(leaderboard: List[Dict]) -> List[Dict]:
	"""
	Function to add stats to each character in the mm+ leaderboard.

	:param leaderboard: A list of characters.
	:return: The same list of characters with a "stats" key added.
	"""
	tasks = []
	async with AsyncClient(timeout=50000000) as client:
		for character in leaderboard:
			tasks.append(asyncio.create_task(
				get_character_details(character.get("region"), character.get("realm_slug"), character.get("name"), client)
			))
		characters_details = await asyncio.gather(*tasks)

	if len(leaderboard) != len(characters_details):
		print(f"ERROR: Not all characters' stats found. "
		      f"leaderboard has len: {len(leaderboard)} and characters_details has len: {len(characters_details)}")

	for character_data, character_details in zip(leaderboard, characters_details):
		character_data["stats"] = character_details["stats"]
		character_data["spec"] = character_details["spec"]

	return leaderboard


