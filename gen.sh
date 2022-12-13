#!/bin/sh

USERS=(
    'alice'
    'bob'
    'carol'
    'dave'
    'eve'
)

for user in "${USERS[@]}"; do
    echo $user
    ./payloadgen.sh $user
done

