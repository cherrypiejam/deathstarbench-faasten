import json, os, sys
import traceback

def handle(req, syscall):
    """Upload user_id and username of the the post creator to Redis and
    optionally invoke compose-post-service-compose-and-upload if all 6 compose
    post functions already completed.
     Args:
        req: a JSON dict with the following fields:
        int req_id (128-bit uuid4 integer)
        string user_id
        string username
        datetime timestamp
    Return:

    """

    if ('username'  not in req or
        'user_id'   not in req or
        'post_info' not in req):
        msg = '''Make sure the input has `username`, `user_id`, `post_info`'''
        return {"status":"MissingFieldError", "message":msg}

    post_info = req['post_info']
    user_id = req['user_id']
    creator_str = json.dumps({"user_id":req['user_id'],
                              "username":req['username']})

    label = syscall.buckle_parse(f'T,{user_id}/app/post')
    creator_path = ['home', label, 'post'] + post_info + ['creator']
    ok = syscall.fs_createfile(creator_path, label) and \
         syscall.fs_write(creator_path, creator_str.encode('utf-8'))
    if not ok:
        return {"status":  "ComposePostServiceUploadCreatorError",
                "message": "Fail to upload creator",
                "traceback": traceback.format_exc()}

    return {"status":"success"}
