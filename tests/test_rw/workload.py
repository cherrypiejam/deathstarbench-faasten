import json, sys, struct
from datetime import datetime

def handle(req, syscall):

    # clean store before calling it

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


    #  if ('arg_1' not in req or
        #  'arg_2' not in req):
        #  return {"status":  "MissingFieldError",
                #  "message": 'Make sure the input has `user_id` and \
                           #  `followee_id` field'}

    #  arg_1 = req['arg_1']
    #  arg_2 = req['arg_2']

    # Current time and label
    #  now = datetime.now()
    #  timestamp = datetime.timestamp(now)
       #  followee_home_dir = ['home', syscall.buckle_parse(f',{user_id}')]
    #  followee_follower_dir = followee_home_dir + ['follower', label]
    #  ok = syscall.fs_createfaceted(followee_follower_dir)
    #  if not ok:
        #  return {"status":  "FollowError",
                #  "message": "Followee not found"}
    #  # TODO More error handling
    #  syscall.fs_createfile(followee_follower_dir + [user_id], label)
    #  syscall.fs_writefile(followee_follower_dir + [user_id], struct.pack('>d', timestamp))

    #  # Add followee to our followee dir
    #  home_dir = ['home', label]
    #  following_dir = home_dir + ['following']
    #  syscall.fs_createfaceted(home_dir) # Make sure dir is ready
    #  syscall.fs_createdir(following_dir, label)
    #  syscall.fs_createfile(following_dir + [followee_id], label)
    #  ok = syscall.fs_writefile(following_dir + [followee_id], struct.pack('>d', timestamp))
    #  print(f'write ok? {ok}')

    #  return dumps({"status": "success", "user": user_ret, "followee":followee_ret})
    return {"status": "success"}
