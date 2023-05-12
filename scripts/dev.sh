#!/bin/bash

pip install -e ./api
pip install llama-cpp-python

redis-server /etc/redis/redis.conf &

# Start the web server
cd web && npm run dev -- --host 0.0.0.0 --port 8008 &
  
# Start the API
cd api && uvicorn src.ayallm.main:api_app --reload --host 0.0.0.0 --port 9124 --root-path /api/ &

# Wait for any process to exit
wait -n
# Exit with status of process that exited first
exit $?
