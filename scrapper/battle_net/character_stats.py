import os
import httpx as requests
from scrapper.exceptions import CharacterNotFound


def get_character_stats(region: str, realm_slug: str, character_name: str) -> dict:
    region = region.lower()
    character_name = character_name.lower()
    api_endpoint = f"https://{region}.api.blizzard.com/profile/wow/character/{realm_slug}/{character_name}/statistics"
    response = requests.get(
        api_endpoint,
        headers={
            'Authorization': f"Bearer {os.environ['BN_JWT']}",
            'Battlenet-Namespace': f'profile-{region}'
        }
    )
    if response.status_code == 404:
        print(f"Skipping {character_name}  {region}-{realm_slug}. 404")
        raise CharacterNotFound
    return response.json()
