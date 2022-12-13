import json, sys, struct
from datetime import datetime

def handle(req, syscall):
    """Add followee_id into the followee list of user_id and add user_id into
    the follower list of the followee_id in the social_graph database
    Args:
        req: request body

        user_id
        followee_id
    """

    begin = datetime.now()

    # The current design is every followee_id/user_id is a file, and each
    # contains a timestamp. Alternatively, we can make them a directory
    # in a timestamp directory for better indexing.

    if ('user_id'     not in req or
        'followee_id' not in req):
        return {"status":  "MissingFieldError",
                "message": 'Make sure the input has `user_id` and \
                           `followee_id` field'}
    user_id = req['user_id']
    followee_id = req['followee_id']

    # TODO check if files already existed in those directory for
    # better error handling

    # Current time and label
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    #  label = syscall.get_current_label()
    label = syscall.buckle_parse(f'T,{user_id}/app/follow')

    # Add user id to followee's follower dir.
    # We do it first because we don't know if their home dir exists and
    # we cannot create one from them. If not there, we fail directly to
    # avoid making further progress.
    followee_home_dir = ['home', syscall.buckle_parse(f'T,{followee_id}/app/follow')]
    followee_follower_dir = followee_home_dir + ['follower', label]
    ok = syscall.fs_createfile(followee_follower_dir + [user_id], label) and \
         syscall.fs_write(followee_follower_dir + [user_id], struct.pack('>d', timestamp))
    if not ok:
        return {"status":  "FollowError",
                "message": "Followee faild to write"}

    # Add followee to our followee dir
    home_dir = ['home', label]
    following_dir = home_dir + ['following']
    ok = syscall.fs_createfile(following_dir + [followee_id], label) and \
         syscall.fs_write(following_dir + [followee_id], struct.pack('>d', timestamp))
    if not ok:
        return {"status":  "FollowError",
                "message": "User faild to write"}

    end = datetime.now()
    return {"status":"success",
            "func":  "social-graph-follow",
            "begin": str(begin),
            "end":   str(end)}
