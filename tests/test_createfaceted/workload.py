import json, sys, struct
from datetime import datetime

def handle(req, syscall):

    # clean store before calling it

    l = syscall.get_current_label()
    print("current label is: ")
    print(l)
    #  print("create faceted dir with current label...")
    #  print(syscall.fs_createfaceted(['home', l, 'somedir']))

    user_id = req['user_id']
    l2 = syscall.buckle_parse(f'T,{user_id}/app/func')
    print("new label is: ")
    print(l2)
    #  print("create faceted dir with new label...")
    #  print(syscall.fs_createfaceted(['home', l2, 'somedir2']))
    #  print(syscall.fs_createdir(['home', l2, 'somedir2', l2, 'somedir3'], l2))

    print("create following dir with new label...")
    print(syscall.fs_createdir(['home', l2, 'following'], l2))
    print("create faceted follower dir with new label...")
    print(syscall.fs_createfaceted(['home', l2, 'follower']))

    return {"status": "success"}
