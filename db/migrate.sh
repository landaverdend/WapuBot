#!/bin/bash
set -e
cd "$(dirname "$0")/.."
source .env
yoyo apply --database "$DATABASE_URL" db/migrations
