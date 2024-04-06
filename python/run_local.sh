#!/bin/bash

set -euo pipefail
IFS=$'\n\t'


docker compose -f docker-compose.yml down
docker compose -f docker-compose.yml up --force-recreate --build
