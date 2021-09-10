import unidecode


def creat_realm_slug(realm_name: str) -> str:
    """
    Create the realm's slug.)
    :param realm_name: The realm name from warcraft log.
    :return: The realm slug.
    """
    # Create realm slug
    server_slug = realm_name.lower().replace("'", "").replace(" ", "-")
    # Remove accents and special chars from realm slug.
    server_slug = unidecode.unidecode(server_slug)
    return server_slug