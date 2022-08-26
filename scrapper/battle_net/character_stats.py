import os
from typing import Dict

from httpx import AsyncClient
from scrapper.exceptions import CharacterNotFound
from scrapper.http_request import get_request_async


async def get_character_stats(region: str, realm_slug: str, character_name: str, client: AsyncClient) -> dict:
    region = region.lower()
    character_name = character_name.lower()
    api_endpoint = f"https://{region}.api.blizzard.com/profile/wow/character/{realm_slug}/" \
                   f"{character_name.replace(' ', '')}/statistics"
    request_headers = {
        'Authorization': f"Bearer {os.environ['BN_JWT']}",
        'Battlenet-Namespace': f'profile-{region}'
    }

    try:
        response_json = await get_request_async(url=api_endpoint, client=client, headers=request_headers)
        if not response_json:
            print(f"Skipping {character_name}  {region}-{realm_slug}. 404")
            raise CharacterNotFound()
        return {
            "mastery": round(response_json["mastery"]["value"], 2),
            "haste": round(response_json["spell_haste"]["value"], 2),
            "crit": round(response_json["spell_crit"]["value"], 2),
            "haste": round(response_json["spell_haste"]["value"], 2),
            "versatility": round(response_json["versatility"], 2),
            "intellect": round(response_json["intellect"]["effective"], 2),
            "agility": round(response_json["agility"]["effective"], 2),
            "strength": round(response_json["strength"]["effective"], 2),
        }
    except BaseException as ex:
        print("STATS FAIL: ", ex)


