import os
import requests


def get_character_stats(region: str, realm_slug: str, character_name: str) -> dict:
    api_endpoint = f"{region}.api.blizzard.com/profile/wow/character/{realm_slug}/{character_name}/statistics"
    response = requests.get(api_endpoint,  headers={'Authorization': f"Bearer {os.environ['BN_JWT']}"})
    return response.json()