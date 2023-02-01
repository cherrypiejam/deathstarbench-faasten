#!/bin/sh

# multivm --config config.yaml --listen_http 127.0.0.1:1337 --listen_sched 127.0.0.1:1338 --mem 500

PIDS=""
scheduler --listen_http 127.0.0.1:1337 --listen_sched 127.0.0.1:1338 &
PIDS="$PIDS $!"
multivm --config config.yaml --listen_sched 127.0.0.1:1338 --mem 500 &
PIDS="$PIDS $!"
trap "kill -2 $PIDS" INT
wait
