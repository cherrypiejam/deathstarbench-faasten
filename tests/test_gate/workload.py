import json, sys, struct
from datetime import datetime

def handle(req, syscall):

    l = syscall.get_current_label()
    print("current label is: ")
    print(l)

    #  print("create faceted dir with current label...")
    #  print(syscall.fs_createfaceted(['home', l, 'somedir']))

    #  user_id = req['user_id']
    #  l2 = syscall.syscall.buckle_parse(f'T,{user_id}')
    #  print("new label is: ")
    #  print(l2)
    #  print("create faceted dir with new label...")
    #  print(syscall.fs_createfaceted(['home', l, 'somedir2', l2]))

    return {"status": "success"}
