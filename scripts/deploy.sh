#!/bin/bash

pip install llama-cpp-python

redis-server /etc/redis/redis.conf &
# Start the API
cd api && uvicorn src.ayallm.main:app --host 0.0.0.0 --port 8008 &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?