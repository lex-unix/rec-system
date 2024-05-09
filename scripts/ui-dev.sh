#!/usr/bin/env fish

load_env .env; or exit
echo ".env file loaded"

npm run dev
