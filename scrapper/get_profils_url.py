from typing import Tuple


def get_character_profile_urls(region: str, realm: str, character_name: str) -> Tuple[str, str, str]:
    """
    Function that generate character's profile for raiderIO and Bnet aromry.

    :param region: Character's region. ex: eu
    :param realm: Character's realm slug. ex: chogall
    :param character_name: Character's name
    :return:
    """
    bnet_armory_profile = f"https://worldofwarcraft.com/en-us/character/{region.lower()}/{realm}/{character_name}"
    raider_io_profile = f"https://raider.io/characters/{region.lower()}/{realm}/{character_name}"
    # TODO: Find a quick way to get warcraftlog ID.
    warcraft_log_profile = f"https://en.warcraftlogs.com/character/{region}/{realm}/{character_name}"

    return bnet_armory_profile, raider_io_profile, warcraft_log_profile


