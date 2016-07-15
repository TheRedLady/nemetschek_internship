#!/bin/bash

# install pgadmin
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install pgadmin3

# install docker
curl -sSL https://get.docker.com/ | sh

# run postgres
docker run --name postgres -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 postgres
docker run -it --rm --link postgres:postgres -v $(pwd):/data  -e "PGPASSWORD=postgres" postgres bash -c 'psql -h postgres -U postgres < /data/dbbook.sql'
