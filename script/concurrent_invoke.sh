#!/bin/sh

USERS=(
    'alice'
    'bob'
    'carol'
    'dave'
    'eve'
)

FAIL=0
PIDS=""


for user in "${USERS[@]}"; do
    cat payloads/payload_$user.jsonl | sfclient --principal $user invoke2 \
             --server 127.0.0.1:1337 > results/concurrent_invoke_$user.txt &
    PIDS="$PIDS $!"
done

for job in $PIDS
do
    wait $job || let "FAIL+=1"
    echo $job $FAIL
done

echo $FAIL

if [ "$FAIL" == "0" ];
then
    echo "YAY!"
else
    echo "FAIL! ($FAIL)"
fi

