# wow-scrapper

This project is a web-app that allows your to scrap data from BattleNet and WarcraftLog APIs.

## Why?
To easily get characters stats from the best players.

## How?
Here are the steps:
1. In the web app you specify which with boss you want to scrap from and with which class/covenant/spec/dps or heal,...
2. The program will query WarcraftLog API to get the top 100 players on this boss with specify params.
3. The program will query BattleNet API to get stat of each player's character.
4. web-app will display the restults.

## Deployement
This repo  is set-up with github actions. Each time you push on `main`, the code will be deployed on production.

## Installation
### Stack
This app uses:
- Python
    - Streamlit (webapp)
    - GraphQL client (request to warcraftLog API).
- Docker (deployement)

### Run the project locally
In order to run the project, I used Docker to avoid installation issues.

All you need to do is:

#### 1. Handle `.env` file 
Decrypt the `.env.gpg` file to get API secrets. (use the passphrase in the 1password). 

**If you don't have it:**
1. Create a file `.env` *(at the root of the project)*
2. Require an API keys to warcraft log and to battle net. Fill `.env` like that:
```bash
# Wacraft log CLIENT ID
WL_CLIENT_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
# Wacraft log CLIENT SECRET
WL_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
WL_AUTH_URL=https://www.warcraftlogs.com/oauth/token
WL_API_GQL_URL=https://www.warcraftlogs.com/api/v2/client

# Battle net CLIENT ID
BN_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Battle net CLIENT SECRET
BN_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
BN_AUTH_URL=https://us.battle.net/oauth/token
```

#### 2. Build the docker image
Install Docker, launch it, then run:
```bash
docker build -t wow_scrapper .
```

#### 3. Run the docker container
Based on the image created, run the container:
```bash
docker run --env-file .env -p 5000:5000 -t wow_scrapper
```

#### 4. Access the app!
The app should be accessile at `localhost:5000`


## API
### Endpoints
#### `GET /`
Check if the  API is live.
**Return**
```json
"Alive"
```

#### `POST /wow-scraper`
Scrap data for a boss and return the best scores.
Made with pagination.
Authorization needed with the classic JWT Bearer token.

**Body**:
```json
{
  "boss_name": ["The Tarragrue", "The  Eye of the  Jailer", "The  Nine", "Remnant of Ner'zhul", "Soulrender Dormazain", "Painsmith Raznal", "Guardian of the First Ones", "Fatescribe Roh-Kalo", "Kel'Thuzad", "Sylvanas Windrunner"],
  "player_class": ["DeathKnight", "Druid", "Hunter", "Mage", "Monk", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior", "DemonHunter"],
  "player_spec": String that matches with player_class. See matching table lower.,
  "covenant_name": ["All", "Kyrian", "Venthyr", "NightFae", "Necrolord"],
  "difficulty_name": ["LFR", "Normal", "Heroic", "Mythic"],
  "role": ["dps", "heal"],
  "result_per_page": int,
  "pagination": int,
}
```

**Class matching with Specs:**
player_spec param need to match with player_class. Only those are possible:
```json
    "DeathKnight": [
        "Unholy",
        "Frost",
        "Blood"
    ],
    "Druid": [
        "Restoration",
        "Balance",
        "Feral",
        "Guardian",
    ],
    "Hunter": [
        "BeastMastery",
        "Marksmanship",
        "Survival"
    ],
    "Mage": [
        "Arcane",
        "Fire",
        "Frost"
    ],
    "Monk": [
        "Brewmaster",
        "Mistweaver",
        "Windwalker"
    ],
    "Paladin": [
        "Holy",
        "Protection",
        "Retribution"
    ],
    "Priest": [
        "Discipline",
        "Holy",
        "Shadow"
    ],
    "Rogue": [
        "Assassination",
        "Subtlety",
        "Outlaw"
    ],
    "Shaman": [
        "Elemental",
        "Enhancement",
        "Restoration"
    ],
    "Warlock": [
        "Affliction",
        "Demonology",
        "Destruction"
    ],
    "Warrior": [
        "Arms",
        "Fury",
        "Protection"
    ],
    "DemonHunter": [
        "Havoc",
        "Vengeance"
    ]
}
```

**Output:**
The outout can be or an error message or the data.

Error message:
```json
{
  "data": {
    "error": "Error message here"
  }
}
```

Date:
```json
{
   "data":[
      {
         "amount":"26 483",
         "covenant":"Necrolord",
         "name":"Bigboat",
         "profiles":{
            "bnet_armory":"https://worldofwarcraft.com/en-us/character/eu/twisting-nether/Bigboat",
            "raider_io":"https://raider.io/characters/eu/twisting-nether/Bigboat"
         },
         "rank":1,
         "server":"Twisting Nether-eu",
         "stats":{
            "agility":386,
            "crit":12.77,
            "haste":22.24,
            "intellect":247,
            "mastery":60.27,
            "strength":1593,
            "versatility":224.0
         }
      },
      {
         "amount":"25 948",
         "covenant":"Necrolord",
         "name":"Cruellaqt",
         "profiles":{
            "bnet_armory":"https://worldofwarcraft.com/en-us/character/eu/twisting-nether/Cruellaqt",
            "raider_io":"https://raider.io/characters/eu/twisting-nether/Cruellaqt"
         },
         "rank":2,
         "server":"Twisting Nether-eu",
         "stats":{
            "agility":370,
            "crit":22.49,
            "haste":15.21,
            "intellect":242,
            "mastery":51.99,
            "strength":1647,
            "versatility":237.0
         }
      },
      {
         "amount":"24 629",
         "covenant":"Necrolord",
         "name":"B\u00f6rny",
         "profiles":{
            "bnet_armory":"https://worldofwarcraft.com/en-us/character/eu/thrall/B\u00f6rny",
            "raider_io":"https://raider.io/characters/eu/thrall/B\u00f6rny"
         },
         "rank":3,
         "server":"Thrall-eu",
         "stats":{
            "agility":385,
            "crit":15.46,
            "haste":20.64,
            "intellect":252,
            "mastery":57.29,
            "strength":1630,
            "versatility":266.0
         }
      },
      {
         "amount":"23 925",
         "covenant":"Necrolord",
         "name":"Tmy",
         "profiles":{
            "bnet_armory":"https://worldofwarcraft.com/en-us/character/eu/draenor/Tmy",
            "raider_io":"https://raider.io/characters/eu/draenor/Tmy"
         },
         "rank":4,
         "server":"Draenor-eu",
         "stats":{
            "agility":370,
            "crit":23.8,
            "haste":19.79,
            "intellect":242,
            "mastery":51.07,
            "strength":1620,
            "versatility":38.0
         }
      },
      {
         "amount":"23 756",
         "covenant":"Necrolord",
         "name":"\u0410\u0432\u0441\u0442\u0435\u0440",
         "profiles":{
            "bnet_armory":"https://worldofwarcraft.com/en-us/character/eu/howling-fjord/\u0410\u0432\u0441\u0442\u0435\u0440",
            "raider_io":"https://raider.io/characters/eu/howling-fjord/\u0410\u0432\u0441\u0442\u0435\u0440"
         },
         "rank":5,
         "server":"\u0420\u0435\u0432\u0443\u0449\u0438\u0439 \u0444\u044c\u043e\u0440\u0434-eu",
         "stats":{
            "agility":381,
            "crit":17.54,
            "haste":20.27,
            "intellect":249,
            "mastery":61.87,
            "strength":1657,
            "versatility":145.0
         }
      },
      {
         "amount":"22 344",
         "covenant":"Necrolord",
         "name":"Spudzindeath",
         "profiles":{
            "bnet_armory":"https://worldofwarcraft.com/en-us/character/eu/tarren-mill/Spudzindeath",
            "raider_io":"https://raider.io/characters/eu/tarren-mill/Spudzindeath"
         },
         "rank":6,
         "server":"Tarren Mill-eu",
         "stats":{
            "agility":370,
            "crit":12.4,
            "haste":15.39,
            "intellect":242,
            "mastery":65.57,
            "strength":1604,
            "versatility":396.0
         }
      },
      {
         "amount":"21 984",
         "covenant":"Necrolord",
         "name":"Deathflagged",
         "profiles":{
            "bnet_armory":"https://worldofwarcraft.com/en-us/character/eu/kazzak/Deathflagged",
            "raider_io":"https://raider.io/characters/eu/kazzak/Deathflagged"
         },
         "rank":7,
         "server":"Kazzak-eu",
         "stats":{
            "agility":381,
            "crit":16.2,
            "haste":22.09,
            "intellect":249,
            "mastery":58.68,
            "strength":1649,
            "versatility":176.0
         }
      },
      {
         "amount":"21 814",
         "covenant":"Necrolord",
         "name":"Purpledk",
         "profiles":{
            "bnet_armory":"https://worldofwarcraft.com/en-us/character/us/stormrage/Purpledk",
            "raider_io":"https://raider.io/characters/us/stormrage/Purpledk"
         },
         "rank":8,
         "server":"Stormrage-us",
         "stats":{
            "agility":404,
            "crit":21.03,
            "haste":12.73,
            "intellect":273,
            "mastery":64.74,
            "strength":1551,
            "versatility":302.0
         }
      },
      {
         "amount":"21 273",
         "covenant":"Necrolord",
         "name":"\u00c9r\u00eab\u00f9s",
         "profiles":{
            "bnet_armory":"https://worldofwarcraft.com/en-us/character/eu/kazzak/\u00c9r\u00eab\u00f9s",
            "raider_io":"https://raider.io/characters/eu/kazzak/\u00c9r\u00eab\u00f9s"
         },
         "rank":9,
         "server":"Kazzak-eu",
         "stats":{
            "agility":383,
            "crit":29.37,
            "haste":7.12,
            "intellect":248,
            "mastery":59.49,
            "strength":1603,
            "versatility":275.0
         }
      },
      {
         "amount":"21 238",
         "covenant":"Necrolord",
         "name":"Sylvann\u00e2h",
         "profiles":{
            "bnet_armory":"https://worldofwarcraft.com/en-us/character/eu/blackmoore/Sylvann\u00e2h",
            "raider_io":"https://raider.io/characters/eu/blackmoore/Sylvann\u00e2h"
         },
         "rank":10,
         "server":"Blackmoore-eu",
         "stats":{
            "agility":374,
            "crit":21.31,
            "haste":14.1,
            "intellect":246,
            "mastery":48.6,
            "strength":1636,
            "versatility":386.0
         }
      }
   ]
}
```