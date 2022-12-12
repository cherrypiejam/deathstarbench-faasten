import json, sys, struct
from datetime import datetime

def handle(req, syscall):
    '''
    This function sets up post directory for a user.
    '''

    user_id = req['user_id']
    label = syscall.buckle_parse(f'T,{user_id}/app/post')
    ok = syscall.fs_createdir(['home', label, 'post'], label)
    if not ok:
        return {"status":  "SetupPostError",
                "message": "Post directory already exists"}

    return {"status": "success"}
