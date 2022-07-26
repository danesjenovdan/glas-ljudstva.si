#!/bin/bash

# EDIT DATABASE NAME TO CHOOSE WHICH ONE YOU WANT
DATABASE_NAME="glasljudstva"

echo "DROPPING THE DB VOLUME"
sudo docker-compose down -v db
sudo docker-compose up -d

sleep 5

echo
echo "LOADING DB INTO CONTAINER"
sudo docker container exec -i $(sudo docker-compose ps -q db) psql -U postgres glasljudstva < db.dump

sudo docker-compose down

echo
echo "ALL DONE, YOU CAN RUN docker-compose up AND/OR DELETE db.dump"
