from scrapper.warcraft_log.warcraft_log_scrapper import scrap_boss
from scrapper.battle_net.realms_list import create_realm_slug_matcher
from scrapper.graph.query_handler import get_Oauth_jwt
import os
import streamlit as st
from scrapper.warcraft_log.sanctum_of_domination import boss_ids
from scrapper.warcraft_log.wow_ids import player_classes_specs, covenant_ids, difficulty_ids

# Generate a JWT for warcraft log that expire in 120 days.
os.environ["WL_JWT"] = get_Oauth_jwt(os.environ["WL_CLIENT_ID"], os.environ["WL_CLIENT_SECRET"], os.environ["WL_AUTH_URL"])
# Generate JWT for BattleNet API.
os.environ["BN_JWT"] = get_Oauth_jwt(os.environ["BN_CLIENT_ID"], os.environ["BN_CLIENT_SECRET"], os.environ["BN_AUTH_URL"])


if __name__ == "__main__":
    # Scrap top 100 players on a specific boss. Get dps or hps and player's stats.
    # scrap_boss("The Nine", "Shaman", "Elemental", "Night Fae", "Heroic")
    #realm_list = create_realm_slug_matcher()
    # print(realm_list)

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


    local_css("style.css")

    st.title("WoW boss scrapper")
    st.write("Welcome to wow boss scrapper, this was made to get the stats of the top 100 players on a boss.")

    # Boss
    boss_name = st.selectbox("Choose your boss:", boss_ids.keys())

    # Class
    class_name = st.selectbox("Choose your class:", player_classes_specs.keys())
    # Spec
    spec_name = st.selectbox("Choose your spec: ", player_classes_specs[class_name])

    # Covenant
    covenant_name = st.selectbox("Choose your covenant: ", covenant_ids.keys())

    # Difficulty
    difficulty_name = st.selectbox("Choose your difficulty: ", difficulty_ids.keys())

    # Role
    role = st.selectbox("DPS or Heal?", ("dps", "heal"))

    # Submit search
    is_scraped = st.button(label="Search")
    
    if is_scraped:

        with st.spinner('Loading data...'):
            # Progress bar
            progress_bar = st.progress(0)
            leader_board = scrap_boss(boss_name, class_name, spec_name, covenant_name, difficulty_name, progress_bar, role)
        for player in leader_board:
            if player['covenant'] == 'All':
                covenant_icon = "<span></span>"
            else:
                covenant_icon = f"<img class='covenant-icon' src='https://assets.rpglogs.com/img/warcraft/abilities/ui_sigil_{player['covenant'].lower()}.jpg'>"
            
            stats_html = f"""
                <div class='player-container'>
                    <div class='player-infos'>
                        <span class='rank'>{player['rank']}.</span>
                        {covenant_icon}
                        <span class='{class_name} bold'>{player['name']}</span>
                        <span class='realm-name'>{player['server']}</span>
                        <span class='bold'>{player['amount']}</span>
                        <span class='profile-icons'>
                           <span> <a target='_blank' href='{player['profiles']['bnet_armory']}'> <img class='covenant-icon' src='https://icon-library.com/images/wow-icon/wow-icon-29.jpg'></a></span>
                           <span> <a target='_blank' href='{player['profiles']['raider_io']}'> <img class='covenant-icon' src='https://cdnassets.raider.io/images/brand/Icon_2ColorWhite.png'></a></span>
                        </span>
                    </div>
                    <div class='stats-container'>
                        <span class='crit'>
                            Crit: <span class='stat-value'>{player['stats']['crit']}</span>
                        </span>  
                        <span class='haste'>
                            Haste: <span class='stat-value'>{player['stats']['haste']}</span>
                        </span>  
                        <span class='mastery'>
                            Mastery: <span class='stat-value'>{player['stats']['mastery']}</span>
                        </span>  
                        <span class='versa'>
                            Versa: <span class='stat-value'>{player['stats']['versatility']}</span>
                        </span>
                    </div>
                </div>
                """
            st.markdown(stats_html, unsafe_allow_html=True)
