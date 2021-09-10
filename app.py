from scrapper.warcraft_log.warcraft_log_scrapper import scrap_boss
from scrapper.graph.query_handler import get_Oauth_jwt
import os

# Generate a JWT for warcraft log that expire in 120 days.
os.environ["WL_JWT"] = get_Oauth_jwt(os.environ["WL_CLIENT_ID"], os.environ["WL_CLIENT_SECRET"], os.environ["WL_AUTH_URL"])
os.environ["BN_JWT"] = get_Oauth_jwt(os.environ["BN_CLIENT_ID"], os.environ["BN_CLIENT_SECRET"], os.environ["BN_AUTH_URL"])
print("BN ", os.environ["BN_JWT"])

if __name__ == "__main__":
    # Example
    scrap_boss("Sanctum of Domination", "The Nine", "Shaman", "Elemental", "Night Fae", "Heroic")




