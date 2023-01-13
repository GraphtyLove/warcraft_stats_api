import os

from httpx import Client
from scrapper.exceptions import CharacterNotFound
from scrapper.http_request import get_request_sync


def get_character_stats(region: str, realm_slug: str, character_name: str, client: Client) -> dict:
    region = region.lower()
    character_name = character_name.lower()
    api_endpoint = f"https://{region}.api.blizzard.com/profile/wow/character/{realm_slug}/" \
                   f"{character_name.replace(' ', '')}/statistics"
    request_headers = {
        'Authorization': f"Bearer {os.environ['BN_JWT']}",
        'Battlenet-Namespace': f'profile-{region}'
    }

    try:
        response_json = get_request_sync(url=api_endpoint, client=client, headers=request_headers)
        if not response_json:
            print(f"Skipping {character_name}  {region}-{realm_slug}. 404")
            raise CharacterNotFound(f"[{region}] {character_name}-{realm_slug} not found.")
        return {
            "stats": {
                "mastery": {
                    "percentage": round(response_json["mastery"]["value"], 2),
                    "value": round(response_json["mastery"]["rating"])
                },
                "haste": {
                    "percentage": round(response_json["spell_haste"]["value"], 2),
                    "value": round(response_json["spell_haste"]["rating"], 2)
                },
                "crit": {
                    "percentage": round(response_json["spell_crit"]["value"], 2),
                    "value": round(response_json["spell_crit"]["rating"], 2)
                },
                "versatility": {"value": round(response_json["versatility"], 2)},
                "main_stats": {
                    "intellect": {"value": round(response_json["intellect"]["effective"], 2)},
                    "agility": {"value": round(response_json["agility"]["effective"], 2)},
                    "strength": {"value": round(response_json["strength"]["effective"], 2)}
                }
            }
        }
    except BaseException as ex:
        print("STATS FAIL: ", ex)


