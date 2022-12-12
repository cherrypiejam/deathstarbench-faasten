import json, sys, struct
from datetime import datetime

def handle(req, syscall):

    l = syscall.get_current_label()
    print("current label is: ")
    print(l)
    print("create dir...")
    print(syscall.fs_createdir(['home', l, 'somedir'], l))
    print("create file...")
    print(syscall.fs_createfile(['home', l, 'somedir', 'somefile'], l))
    print("write file...")
    print(syscall.fs_write(['home', l, 'somedir', 'somefile'], 'sometext'.encode('utf-8')))
    print("read file...")
    print(syscall.fs_read(['home', l, 'somedir', 'somefile']))

    print("delete file...")
    print(syscall.fs_delete(['home', l, 'somedir', 'somefile']))
    print("write file...(SHOULD FAIL)")
    print(syscall.fs_write(['home', l, 'somedir', 'somefile'], 'sometext'.encode('utf-8')))
    print("read file...(SHOULD FAIL)")
    print(syscall.fs_read(['home', l, 'somedir', 'somefile']))

    print("delete dir...")
    print(syscall.fs_delete(['home', l, 'somedir']))
    print("create file...(SHOULD FAIL)")
    print(syscall.fs_createfile(['home', l, 'somedir', 'somefile'], l))


    return {"status": "success"}
