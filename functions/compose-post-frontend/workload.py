import concurrent.futures
import json
from datetime import datetime
import uuid

def upload_creator(post_info, user_id, username, syscall):
    '''
    return a bool
    '''
    req = {"post_info": post_info,
           "user_id":   user_id,
           "username":  username} # FIXME need username?
    gate = ['home',
            syscall.buckle_parse(f'T,{user_id}'),
            "compose-post-service-upload-creator"]
    return syscall.invoke(gate, json.dumps(req))

def upload_media(post_info, user_id, media_type, media_id, syscall):
    '''
    return a bool
    '''
    req = {"post_info":  post_info,
           "user_id":    user_id,
           "media_id":   media_id,
           "media_type": media_type}
    gate = ['home',
            syscall.buckle_parse(f'T,{user_id}'),
            "compose-post-service-upload-media"]
    return syscall.invoke(gate, json.dumps(req))

def upload_text(post_info, user_id, text, syscall):
    '''
    return a bool
    '''
    req = {"post_info": post_info,
           "user_id":   user_id,
           "text":      text}
    gate = ['home',
            syscall.buckle_parse(f'T,{user_id}'),
            "text-service-upload-text"]
    return syscall.invoke(gate, json.dumps(req))

def handle(req, syscall):
    """handle a request to the function
    Args:
        req: a JSON with the following fields:
            string user_id
            string username
            number post_type
            string text
            string media_id
            string media_type
    Return:
        on success, return {"status": "success", ...TBD}
        on error, return {"status": "ComposePostFrontError", "errors": [errors from
        each function call]}
    """

    if ('username'   not in req or
        'user_id'    not in req or
        'post_type'  not in req or
        'text'       not in req or
        'media_id'   not in req or
        'media_type' not in req):
        msg = '''Make sure the input has `username`, `user_id`, `post_type`,
        `text`, `media_id` and `media_type` fields'''
        return {"status": "MissingFieldError",
                "errors": [msg]}

    user_id = req['user_id']
    post_type = req['post_type']
    post_id = uuid.uuid4().int
    now = datetime.now()
    post_info = [
        item if isinstance(item, str) else str(item)
        for item in [
            post_type, now.year, now.month, now.day,
            now.hour, now.minute, now.second, post_id,
        ]
    ]

    # Current label
    label = syscall.buckle_parse(f'T,{user_id}/app/post')
    post_dir = ['home', label, 'post'] + post_info

    post_path = f':home:T,{user_id}/app/post:post:'+':'.join(post_info)
    print(post_path)

    # Ensures to have the home directory and
    # prepare for the post directory
    for i in range(3, len(post_dir)):
        syscall.fs_createdir(post_dir[:i], label)
    ok = syscall.fs_createdir(post_dir, label)
    if not ok:
        return {"status":  "ComposePostFrontError",
                "message": "Fail to create a post"}

    ok = upload_creator(post_info, user_id, req['username'], syscall) and \
         upload_media(post_info, user_id, req['media_type'], req['media_id'], syscall) and \
         upload_text(post_info, user_id, req['text'], syscall)
    if not ok:
        return {"status":  "ComposePostFrontError",
                "message": "Fail to invoke functions"}
    return {"status":   "success",
            "post_path": post_path}

    #  futures = []
    #  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        #  futures.append(executor.submit(upload_creator,
            #  post_info, user_id, req['username'], syscall))
        #  futures.append(executor.submit(upload_media,
            #  post_info, user_id, req['media_type'], req['media_id'], syscall))
        #  futures.append(executor.submit(upload_text,
            #  post_info, user_id, req['text'], syscall))

        #  # Results only give if functions are successfully invoked
        #  results = [f.result() for f in concurrent.futures.as_completed(futures)]

        #  if not all(results):
            #  return {"status":  "ComposePostFrontError",
                    #  "message": "Fail to invoke functions"}

        #  return {"status":   "success",
                #  "post_path": post_path}
