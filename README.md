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
Decrypt the `.env.gpg` file to get API secrets. (use the passephrase in the 1password). 

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
