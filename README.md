# Warcraft Stats - Back end

Warcraft Stat is a web-site that allow you to track best players' statistics on their character.

It has been developed to facilitate the tedious process of wondering which stats pros are prioritizing on their class.


## Project

This repo is only the back-end, you can find the front-end (an SPA built with React) in the link bellow.

**[FRONT END](https://github.com/GraphtyLove/warcraft_stats_frontend)**


## Stack

- `Python 3.10` with MyPy typing
- `FastApi 0.80` with auto-generated doc


## How?

Here are the steps:
1.  You specify to the API which with boss you want to scrap from and with which class/spec/dps or heal,...
2. The program will query WarcraftLog API to get the top 100 players on this boss with specify params.
3. The program will query BattleNet API to get stat of each player's character.
4. The API will display the results.


## Deployement

This repo is set-up with github actions. Each time you push on `main`, the code will be deployed on production.


## Installation

### Stack

This app uses:
- Python
    - FastApi
    - Swagger (API documentation)
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
docker build -t warcraft_stats_api .
```


#### 3. Run the docker container

Based on the image created, run the container:
```bash
docker run --env-file .env -p 8000:8000 -t warcraft_stats_api
```


#### 4. Access the API's documentation!

The API should be accessible at `localhost:8000/docs`


#### 5. Access the API!

The API should be accessible at `localhost:8000`


## Contributing

If you would like to add something to the project, feel free to open a Pull-Request!