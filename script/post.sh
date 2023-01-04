#!/bin/sh
sfclient --principal alice invoke --gate :home:T,alice:compose-post-frontend --server 127.0.0.1:1337 < payloads/compose-post-frontend.json
