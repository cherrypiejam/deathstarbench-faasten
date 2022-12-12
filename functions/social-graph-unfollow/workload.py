import sys, json
from datetime import datetime

def handle(req, syscall):
    """Remove followee_id from the followee list of user_id and remove user_id
    from the follower list of the followee_id in the social_graph database
    Args:
        req: request body

        user_id
        followee_id
    """

    if ('user_id'     not in req or
        'followee_id' not in req):
        return {"status":  "MissingFieldError",
                "message": 'Make sure the input has `user_id` and\
                           `followee_id` field'}
    user_id = req['user_id']
    followee_id = req['followee_id']

    # Current date and time
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    #  label = syscall.get_current_label()
    label = syscall.buckle_parse(f'T,{user_id}/app/follow')

    followee_home_dir = ['home', syscall.buckle_parse(f'T,{followee_id}/app/follow')]
    followee_follower_dir = followee_home_dir + ['follower', label]
    ok = syscall.fs_delete(followee_follower_dir + [user_id])
    if not ok:
        return {"status":  "UnfollowError",
                "message": "Followee failed to delete"}

    following_dir = ['home', label, 'following']
    ok = syscall.fs_delete(following_dir + [followee_id])
    if not ok:
        return {"status":  "UnfollowError",
                "message": "Failed to unfollow"}

    return {"status": "success"}
