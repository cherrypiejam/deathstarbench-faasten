#!/bin/sh

multivm --config config.yaml --listen_http 127.0.0.1:1337 --listen_sched 127.0.0.1:1338 --mem 500
