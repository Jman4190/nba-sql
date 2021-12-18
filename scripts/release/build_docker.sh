#!/bin/bash
## Script to build an executable in a linux container.
rm -rf build/ dist/
mkdir dist

DOCKER_BUILDKIT=1 docker build --tag nba-sql-builder -f docker/Dockerfile.build .

DIST_PATH="$PWD/dist"

docker run -v $DIST_PATH:/app/dist/ nba-sql-builder
