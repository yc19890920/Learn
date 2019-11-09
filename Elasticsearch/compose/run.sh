#!/usr/bin/env bash

mkdir -p $(pwd)/data/{es01,es02,es03}
mkdir -p $(pwd)/logs/{es01,es02,es03}

chmod -R 775 $(pwd)/data/{es01,es02,es03}  $(pwd)/logs/{es01,es02,es03}

docker-compose up -d

docker-compose ps