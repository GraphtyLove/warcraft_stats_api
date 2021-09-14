#!/bin/bash
set -e;

echo "Deploying wow scraper...";
cd /home/maxim/production/wow-scrapper;
whoami;
git pull;
docker build -t wow_scraper;
docker stop wow_scraper;
docker run -d --env-file .env -p 5000:5000 -t wow_scraper;
echo "🚀 Wow scraper deployed!";