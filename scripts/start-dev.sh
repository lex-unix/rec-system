#!/usr/bin/env fish

set -l services db redis
set -l running_containers (docker compose ps --format "{{.Names}}")
set -l not_running false

for service in $services
  if not string match -q "*-$service-*" $running_containers
    echo "Starting service: $service"
    docker compose up -d $service
    set not_running true
  end
end

if not $not_running
  echo "All containers are already running."
end

load_env .env; or exit
echo ".env file loaded"

poetry run uvicorn app.main:app --reload
