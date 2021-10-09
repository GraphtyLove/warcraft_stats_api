from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from jwt_utils.check_jwt import check_jwt
from scrapper.graph.query_handler import get_Oauth_jwt
from scrapper.warcraft_log.warcraft_log_scrapper import scrap_boss

# Generate a JWT for warcraft log that expire in 120 days.
os.environ["WL_JWT"] = get_Oauth_jwt(os.environ["WL_CLIENT_ID"], os.environ["WL_CLIENT_SECRET"], os.environ["WL_AUTH_URL"])
# Generate JWT for BattleNet API.
os.environ["BN_JWT"] = get_Oauth_jwt(os.environ["BN_CLIENT_ID"], os.environ["BN_CLIENT_SECRET"], os.environ["BN_AUTH_URL"])


app = Flask(__name__)
# Enable cors
CORS(app)



@app.route("/", methods=["GET"])
def home():
    """
    Route to check if the server  runs.
    """
    return "alive"


@app.route("/wow_scraper", methods=["POST"])
def wow_scraper():
    """
    Route that will scrap top 100 players on a specific boss with specific conditions.
    """

    encoded_jwt = request.headers.get('Authorization', None)
    if not encoded_jwt:
        return jsonify({"error": "User not connected."})

    is_token_valid = check_jwt(encoded_jwt.replace("Bearer ", ""))
    if not is_token_valid:
        return jsonify({"error": "Invalid token."})

    try:
        # Get params from request
        boss_name = request.json.get("boss_name").strip()
        player_class = request.json.get("player_class").strip()
        player_spec = request.json.get("player_spec").strip()
        covenant_name = request.json.get("covenant_name").strip()
        difficulty_name = request.json.get("difficulty_name").strip()
        role = request.json.get("role").strip()
    except AttributeError:
        return jsonify({"error": "param missing"})
    try:
        result_per_page = int(request.json.get("result_per_page").strip())
    except AttributeError:
        result_per_page = 10
    try:
        pagination = int(request.json.get("pagination").strip())
    except AttributeError:
        pagination = 1

    # Scrap data.
    leader_board = scrap_boss(
        boss_name,
        player_class,
        player_spec,
        covenant_name,
        difficulty_name,
        role=role,
        result_per_page=result_per_page,
        pagination=pagination
    )

    return jsonify({"data": leader_board})




# * -------------------- RUN SERVER -------------------- *
if __name__ == "__main__":
    # * --- DEBUG MODE: --- *
    app.run(host="0.0.0.0", debug=True)
    # * --- PROD MODE: --- *
    # app.run(host='0.0.0.0')
