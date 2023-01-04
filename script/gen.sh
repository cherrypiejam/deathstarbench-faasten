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
    ./script/payloadgen.sh $user
done

