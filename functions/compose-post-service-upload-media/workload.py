import json, os, sys
import traceback

def handle(req, syscall):
    """Upload media_id and media_type to Redis and optionally invoke
    compose-post-service-compose-and-upload if all 6 compose post functions
    already completed.
     Args:
        req (dict): a JSON dict with the following fields:
            int req_id (128-bit uuid4 integer)
            string media_id
            string media_type
    Return:

    """

    if ('media_type' not in req or
        'media_id'   not in req or
        'user_id'    not in req or
        'post_info'  not in req):
        msg = '''Make sure the input has `media_type`, `media_id`, `post_info`, `user_id`'''
        return {"status":"MissingFieldError", "message":msg}

    post_info = req['post_info']
    user_id = req['user_id']
    if req['media_id'] == None:
        media_str = json.dumps({})
    else:
        media_str = json.dumps({"media_id":req['media_id'],
                                "media_type":req['media_type']})

    label = syscall.buckle_parse(f'T,{user_id}/app/post')
    media_path = ['home', label, 'post'] + post_info + ['media']
    ok = syscall.fs_createfile(media_path, label) and \
         syscall.fs_write(media_path, media_str.encode('utf-8'))
    if not ok:
        return {"status":  "ComposePostServiceUploadMediaError",
                "message": "Fail to upload media",
                "traceback": traceback.format_exc()}

    return {"status":"success"}
