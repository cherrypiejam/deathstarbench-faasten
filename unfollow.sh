#!/bin/sh
sfclient --principal alice invoke --gate :home:T,alice:social-graph-unfollow --server 127.0.0.1:1337 < payloads/follow.json
