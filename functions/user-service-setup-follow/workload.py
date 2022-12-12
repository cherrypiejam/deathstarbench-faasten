import json, sys, struct
from datetime import datetime

def handle(req, syscall):
    '''
    This function sets up a following and a faceted follower
    directory for a user.
    '''

    user_id = req['user_id']
    label = syscall.buckle_parse(f'T,{user_id}/app/follow')
    ok = syscall.fs_createdir(['home', label, 'following'], label) and \
         syscall.fs_createfaceted(['home', label, 'follower'])
    if not ok:
        return {"status":  "SetupFollowError",
                "message": "Following/follower directory already exists"}

    return {"status": "success"}
