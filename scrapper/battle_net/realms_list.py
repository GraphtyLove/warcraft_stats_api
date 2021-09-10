import os
import requests
import json

REALM_MATCHER_FILE_PATH = "scrapper/battle_net/realm_slug_matcher.json"


def create_realm_slug_matcher() -> None:
    """
    Function that query BattleNet API to get a list of realm with their slug.
    Used to get slug of realms and query the character API.

    By default, I get get the list of realm from US and EU and merge them.
    """
    regions = ["eu", "us"]
    realms_name_to_slug_matcher = {}
    for region in regions:
        api_endpoint = f"https://{region}.api.blizzard.com/data/wow/realm/index?namespace=dynamic-{region}"
        response = requests.get(api_endpoint,  headers={'Authorization': f"Bearer {os.environ['BN_JWT']}"})

        realm_list = response.json()
        realm_list = realm_list["realms"]

        for realm in realm_list:
            region_name_list = realm["name"]
            for region_name in region_name_list.values():
                realms_name_to_slug_matcher[region_name] = realm["slug"]

    with open(REALM_MATCHER_FILE_PATH, 'w', encoding='utf-8') as file:
        # ensure_ascii False to allow russian and asian chars.
        json.dump(realms_name_to_slug_matcher, file, ensure_ascii=False)

    print(f"Realm slug matcher made for: {regions} written at: {REALM_MATCHER_FILE_PATH}")


def get_realm_slug(realm_name: str) -> str:
    """
    Get the realm's slug based on the list of realm's slug made with get_realm_list().

    :param realm_name: The realm name from warcraft log.
    :return: The realm slug.
    """
    with open(REALM_MATCHER_FILE_PATH) as file:
        realm_matcher = json.load(file)
        realm_slug = realm_matcher[realm_name]
    return realm_slug
