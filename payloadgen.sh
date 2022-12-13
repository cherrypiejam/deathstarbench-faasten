#!/bin/sh

USERS=(
    'alice'
    'bob'
    'carol'
    'dave'
    'eve'
)

GATES=(
    'social-graph-follow'
    'social-graph-unfollow'
    'compose-post-frontend'
)

PRINCIPAL="$1"
OUTFILE="payloads/payload_$1.jsonl"

echo -n > $OUTFILE
for (( i=0; i<1000; i++ )); do

    gate=${GATES[ $RANDOM % ${#GATES[@]} ]}
    gate=":home:T,$PRINCIPAL:$gate" # Path
    sleeptime=$(( ( RANDOM % 5 ) + 1 ))
    while
        user=${USERS[ $RANDOM % ${#USERS[@]} ]}
        [[ "$user" == "$PRINCIPAL" ]]
    do :; done

    case $gate in
        *-follow | *-unfollow)
            payload="{\\\"user_id\\\":\\\"$PRINCIPAL\\\",\\\"followee_id\\\":\\\"$user\\\"}"
            echo "{\"path\":\"$gate\",\"sleep_ms\":$sleeptime,\"payload\":\"$payload\"}" >> $OUTFILE
            ;;
        *-post-frontend)
            payload="{\\\"user_id\\\": \\\"$PRINCIPAL\\\", \\\"username\\\":\\\"$PRINCIPAL\\\", \\\"post_type\\\": 0, \\\"text\\\":\\\"ABC's Trump In Trouble Poll Surveyed Just 533, Not Likely Voters, Asked Over 20% More Biden Supporters Than Conservatives https://thenationalpulse.com/news/abcs-trump-in-trouble-poll-surveyed-just-533-not-likely-voters-asked-over-20-more-biden-supporters-than-conservatives/ via @TheNatPulse Total Fake Poll. @ABCNews https://abc.com is just like the rest of them! @realDonaldTrump\\\", \\\"media_id\\\": \\\"APicture\\\", \\\"media_type\\\": \\\"png\\\"}"
            echo "{\"path\":\"$gate\",\"sleep_ms\":$sleeptime,\"payload\":\"$payload\"}" >> $OUTFILE
            ;;
        *) echo "unknown" ;;
    esac

done
