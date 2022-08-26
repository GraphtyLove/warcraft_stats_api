import asyncio

from fastapi import FastAPI, Query
import os

from custom_types.api_response import ErrorResponse, SuccessResponse
from custom_types.class_and_specs import ClassName, SpecName
from custom_types.player_role_types import PlayerRole
from custom_types.raid_types import RaidName, BossName, RaidDifficulty
from custom_types.region import Region
from custom_types.shadowland_types import CovenantName
from scrapper.graph.query_handler import get_Oauth_jwt
from scrapper.raider_io.mythic_plus_leaderboard import (
    get_leaderboard_for_class_and_spec,
    add_character_stats_to_leaderboard
)
from scrapper.warcraft_log.warcraft_log_scrapper import scrap_boss
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Generate a JWT for warcraft log that expire in 120 days.
os.environ["WL_JWT"] = get_Oauth_jwt(os.environ["WL_CLIENT_ID"], os.environ["WL_CLIENT_SECRET"], os.environ["WL_AUTH_URL"])
# Generate JWT for BattleNet API.
os.environ["BN_JWT"] = get_Oauth_jwt(os.environ["BN_CLIENT_ID"], os.environ["BN_CLIENT_SECRET"], os.environ["BN_AUTH_URL"])


app = FastAPI()


@app.get("/")
def home():
    """
    Route to check if the server  runs.
    """
    return "alive"


@app.get("/mythic-plus")
def mythic_plus(
        class_name: ClassName,
        spec_name: SpecName,
        region: Region = "world",
        season: str = "season-sl-4",
        max_characters: int = Query(title="Number of Characters checked.", gt=0, le=100, default=60)
):
    raider_io_leaderboard = asyncio.run(
        get_leaderboard_for_class_and_spec(class_name, spec_name, region, season, max_characters)
    )
    return {"data": raider_io_leaderboard}


@app.get("/raid")
def raid_scraper(
        raid_name: RaidName,
        boss_name: BossName,
        player_class: ClassName,
        player_spec: SpecName,
        covenant_name: CovenantName,
        difficulty_name: RaidDifficulty,
        role: PlayerRole,
        result_per_page: int = Query(title="Max characters per page", gt=0, le=50, default=10),
        page: int = Query(title="Page number", gt=0, default=1)
) -> SuccessResponse | ErrorResponse:
    """
    Route that will scrap top 100 players on a specific boss with specific conditions.
    """
    # Scrap data.
    leader_board = scrap_boss(
        raid_name,
        boss_name,
        player_class,
        player_spec,
        covenant_name,
        difficulty_name,
        role=role,
        result_per_page=result_per_page,
        pagination=page
    )
    # In case scrap_boss return an error
    if isinstance(leader_board, str):
        return {"error": leader_board}

    return {"data": leader_board}

