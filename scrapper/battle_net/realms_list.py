import os
import requests


def get_character_stats(region: str, namespace: str) -> dict:
    api_endpoint = f"https://{region}.api.blizzard.com/data/wow/realm/index "
    response = requests.get(api_endpoint,  headers={'Authorization': f"Bearer {os.environ['BN_JWT']}"})
    return response.json()
