import json, sys, struct
from datetime import datetime

def handle(req, syscall):

    # clean store before calling it

    l = syscall.get_current_label()
    print("current label is: ")
    print(l)

    user_id = req['user_id']
    followee_id = req['followee_id']
    l2 = syscall.buckle_parse(f'T,{user_id}/app/func')
    print("new label is: ")
    print(l2)

    l3 = syscall.buckle_parse(f'T,{followee_id}/app/func')
    print("another label is: ")
    print(l3)

    print("create my file with new label...")
    print(syscall.fs_createfile(['home', l3, 'follower', l2, f'{user_id}'], l2))

    return {"status": "success"}
