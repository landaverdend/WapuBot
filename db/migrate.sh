#!/bin/bash
set -e
cd "$(dirname "$0")/.."
source .env
yoyo apply --batch --database "$DATABASE_URL" db/migrations
