import json, os, sys
from datetime import datetime

def handle(req, syscall):
    """Upload post text with shortened urls to Redis and optionally invoke
    compose-post-service-compose-and-upload if all 6 compose post functions
    already completed.
    Args:
        req: a JSON dict with the following fields:
        int req_id (128-bit uuid4 integer)
        str text
    Return:

    """
    begin = datetime.now()

    if ('text'      not in req or
        'user_id'   not in req or
        'post_info' not in req):
        msg = '''Make sure the input has `text`, `user_id` and `post_info`'''
        return {"status":"MissingFieldError", "message":msg}

    post_info = req['post_info']
    user_id = req['user_id']
    text = req['text']

    label = syscall.buckle_parse(f'T,{user_id}/app/post')
    text_path = ['home', label, 'post'] + post_info + ['text']
    ok = syscall.fs_createfile(text_path, label) and \
         syscall.fs_write(text_path, text.encode('utf-8'))
    if not ok:
        return {"status":  "ComposePostServiceUploadTextError",
                "message": "Fail to upload the text"}

    end = datetime.now()
    return {"status":"success",
            "func":  "post-upload-text",
            "begin": str(begin),
            "end":   str(end)}
