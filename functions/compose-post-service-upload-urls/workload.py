import json
from datetime import datetime
import traceback

def handle(req, syscall):
    """Upload full and shortened urls to Redis and optionally invoke
    compose-post-service-compose-and-upload if all 6 compose post functions
    already completed.
     Args:
        req (dict): a JSON dict with the following fields:
            int req_id (128-bit uuid4 integer)
            list(JSON_str) urls
    Return:

    """
    begin = datetime.now()

    if ('urls'      not in req or
        'user_id'   not in req or
        'post_info' not in req):
        msg = '''Make sure the input has `urls`, `user_id` and `post_info`'''
        return {"status":"MissingFieldError", "message":msg}

    post_info = req['post_info']
    user_id = req['user_id']
    urls_str = json.dumps(req['urls'])

    label = syscall.buckle_parse(f'T,{user_id}/app/post')
    urls_path = ['home', label, 'post'] + post_info + ['urls']
    ok = syscall.fs_createfile(urls_path, label) and \
         syscall.fs_write(urls_path, urls_str.encode('utf-8'))
    if not ok:
        return {"status":  "ComposePostServiceUploadUrlsError",
                "message": "Fail to upload urls",
                "traceback": traceback.format_exc()}

    end = datetime.now()
    return {"status":"success",
            "func":  "post-upload-urls",
            "begin": str(begin),
            "end":   str(end)}
