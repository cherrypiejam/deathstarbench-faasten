#!/bin/sh

USERS=(
    'alice'
    # 'bob'
    # 'carol'
)
SETUP_GATES=(
    'user-service-setup-follow'
    'user-service-setup-post'
)
FUNCTION_DIR="$(pwd)/functions"

function create_all_gates {
    for user in "${USERS[@]}"; do
        for function in $(ls $FUNCTION_DIR); do
            # setup gates
            invk="$user"
            case "$function" in
                "user-service-setup-follow"*) func='follow';;
                "social-graph"*)              func='follow';;
                "media-front"*)               func='media' ;;
                "user-service-setup-post"*)   func='post'  ;;
                "compose-post-frontend"*)     func='post'  ;;
                *)                            func='post'; invk="$user/app/$func";;
            esac
            # echo $function "--" $user $func $invk
            echo "setup $function for $user..."
            sfclient --principal $user newgate \
                     --base-dir  :home         \
                     --function  $function     \
                     --gate-name $function     \
                     --policy    "$user/app/$func,$invk"
        done
    done
}

function invoke_setup_gates {
    for user in "${USERS[@]}"; do
        for gate in "${SETUP_GATES[@]}"; do
            echo "invoking $gate for $user..."
            echo "{\"user_id\":\"$user\"}" |             \
                sfclient --principal $user invoke        \
                         --gate      :home:T,$user:$gate \
                         --server    127.0.0.1:1337
        done
    done
}

if [ "$1" == "create" ]; then
    create_all_gates
elif [ "$1" == "invoke" ]; then
    invoke_setup_gates
else
    # rm storage/*
    create_all_gates
    invoke_setup_gates
fi



