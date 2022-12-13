import json, os, sys
from datetime import datetime

def handle(req, syscall):
    """Upload user mentions (user_id and username) in the post text to Redis and
    optionally invoke compose-post-service-compose-and-upload if all 6
    compose post functions already completed.
    Args:
        req (dict): a JSON dict with the following fields:
        int req_id (128-bit uuid4 integer)
        list(dict) user_mentions each user_mention is a dict of the form
        {"username": username, "user_id": user_id}
    Return:

    """
    begin = datetime.now()

    if ('user_mentions' not in req or
        'user_id'       not in req or
        'post_info'     not in req):
        msg = '''Make sure the input has `user_mentions`, `user_id` and `post_info`'''
        return {"status":"MissingFieldError", "message":msg}

    post_info = req['post_info']
    user_id = req['user_id']
    user_mentions = req['user_mentions']

    label = syscall.buckle_parse(f'T,{user_id}/app/post')
    user_mentions_path = ['home', label, 'post'] + post_info + ['user_mentions']
    ok = syscall.fs_createfile(user_mentions_path, label) and \
         syscall.fs_write(user_mentions_path,
                          json.dumps(user_mentions).encode('utf-8'))
    if not ok:
        return {"status":  "ComposePostServiceUploadUserMentionsError",
                "message": "Fail to upload user mentions"}

    end = datetime.now()
    return {"status":"success",
            "func":  "post-upload-user-mentions",
            "begin": str(begin),
            "end":   str(end)}
