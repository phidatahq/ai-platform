#!/bin/bash

set -e

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_ROOT="$(dirname "$(dirname "$(dirname ${CURR_DIR})")")"
DOCKER_FILE="${CURR_DIR}/Dockerfile"
REPO="repo"
NAME="airflow-dp"
TAG="dev"

# Run docker buildx create --use before running this script
echo "Running: docker buildx build --platform=linux/amd64 -t $REPO/$NAME:$TAG -f $DOCKER_FILE $WS_ROOT --push"
docker buildx build --platform=linux/amd64 -t $REPO/$NAME:$TAG -f $DOCKER_FILE $WS_ROOT --push
