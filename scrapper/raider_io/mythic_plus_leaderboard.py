import asyncio
from math import ceil
from typing import Dict, List
from httpx import AsyncClient

from custom_types.class_and_specs import ClassName, SpecName
from custom_types.region import Region
from scrapper.exceptions import ApiDataError
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

		covenant_icon_slug = character_data.get("covenant", {}).get("icon"),
		bnet_profile_path = character_data.get("path")
		realm_region = realm_data.get("locale")

		formatted_characters.append({
			"name": character_data.get("name"),
			"realm": realm_data.get("name"),
			"bnet_profile_link": f"https://worldofwarcraft.com/{realm_region}{bnet_profile_path}",
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
		max_players: int = 60
) -> List[Dict]:
	# RaiderIo API returns 20 players per page
	player_per_page = 20
	number_of_pages = ceil(max_players / player_per_page)

	leaderboard = []
	tasks = []
	async with AsyncClient() as client:
		for page_number in range(number_of_pages):
			page_url = format_leaderboard_request_url(class_name, spec_name, region, season, page_number)
			tasks.append(asyncio.create_task(
				get_request_async(url=page_url, client=client)
			))

		pages_data = await asyncio.gather(*tasks)

	for page_data in pages_data:
		leaderboard.extend(format_leaderboard_page_results(page_data))
	return leaderboard



