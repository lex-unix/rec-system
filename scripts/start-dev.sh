#!/usr/bin/env fish

load_env .env; or exit

echo ".env file loaded"

uvicorn app.main:app --reload
