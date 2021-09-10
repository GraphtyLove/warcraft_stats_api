import os
import requests
from scrapper.battle_net.utils import creat_realm_slug


def get_character_stats(region: str, realm_name: str, character_name: str) -> dict:
    region = region.lower()
    character_name = character_name.lower()
    realm_slug = creat_realm_slug(realm_name)
    
    api_endpoint = f"https://{region}.api.blizzard.com/profile/wow/character/{realm_slug}/{character_name}/statistics"
    print(api_endpoint)
    response = requests.get(
        api_endpoint,
        headers={
            'Authorization': f"Bearer {os.environ['BN_JWT']}",
            'Battlenet-Namespace': f'profile-{region}'
        }
    )
    return response.json()
