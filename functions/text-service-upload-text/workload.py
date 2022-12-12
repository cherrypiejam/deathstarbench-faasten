import concurrent.futures
import json
import re
import random
import string

HOSTNAME="http://short-u.rl/"

user_mention_pattern = re.compile(r"@[a-zA-Z0-9]+")
url_pattern=re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def upload_urls(post_info, user_id, urls, syscall):
    '''
    Args:
        urls: a list of str of urls. urls can be the empty list
    '''
    req = {"post_info": post_info,
           "user_id":   user_id,
           "urls":      urls}
    gate = ['home',
            syscall.buckle_parse(f'T,{user_id}'),
            "compose-post-service-upload-urls"]
    return syscall.invoke(gate, json.dumps(req))

def upload_user_mentions(post_info, user_id, user_mentions, syscall):
    '''
    user_mentions: a list of usernames ste each with an @ sign prefix
    '''
    req = {"post_info":     post_info,
           "user_id":       user_id,
           "user_mentions": user_mentions}
    gate = ['home',
            syscall.buckle_parse(f'T,{user_id}'),
            "compose-post-service-upload-user-mentions"]
    return syscall.invoke(gate, json.dumps(req))

def upload_text(post_info, user_id, text, syscall):
    req = {"post_info": post_info,
           "user_id":   user_id,
           "text":      text}
    gate = ['home',
            syscall.buckle_parse(f'T,{user_id}'),
            "compose-post-service-upload-text"]
    return syscall.invoke(gate, json.dumps(req))

def handle(req, syscall):
    """Process the text in a post
    Extract the user mentions and urls that might appear in the text of a post.
    Forwards user mentions (a list of username strings) to
    user-mention-service-upload-user-mentions and the urls (a list of url
    strings) to url-shorten-service-upload-urls. After
    url-shorten-service-upload-urls returns shortened urls, replace full urls in
    the original text with shortened urls and send the new text to
    compose-post-service-upload-text for uploading.
    Args:
        req (dict): a dict with the following fields:
            int req_id (128-bit uuid4 integer)
            str text
    Return:
        on success, return {"status": "success", ...TBD}
        on error, return {"status": "TextServiceUploadTextError", "errors": [errors from
        each function call]}
    """

    if ('post_info' not in req or
        'user_id'   not in req or
        'text'      not in req):
        msg = '''Make sure the input has `post_info`, `user_id` and `text` fields'''
        return {"status":"MissingFieldError", "errors":[msg]}

    post_info = req['post_info']
    user_id = req['user_id']
    text = req['text']

    user_mentions = user_mention_pattern.findall(text)
    user_mentions = [u[1:] for u in user_mentions if u[0] == "@"]

    # TODO We also need to store the mapping
    # /home/<label>/urls/shorten <- long-urls
    # We can pass storing part to a function
    urls = url_pattern.findall(text)
    url_match_obj_list= list(url_pattern.finditer(text))
    url_doc_list = []
    for u in urls:
        url_doc_list.append({"expanded_url": u,
                             "shortened_url": HOSTNAME+get_random_string(10)})

    # Update text by replacing original full urls with shortened urls
    for url_doc, url_match_obj in zip(reversed(url_doc_list),
            reversed(url_match_obj_list)):
        prefix = text[0:url_match_obj.start()]
        suffix = text[url_match_obj.end():]
        text = prefix + url_doc['shortened_url'] + suffix


    ok = upload_text(post_info, user_id, text, syscall) and \
         upload_user_mentions(post_info, user_id, user_mentions, syscall) and \
         upload_urls(post_info, user_id, user_mentions, syscall)
    if not ok:
        return {"status":  "TextServiceUploadTextError",
                "message": "Fail to invoke functions"}

    return {"status": "success"}

    #  # Call compose-post-service-upload-user-mentions and
    #  # compose-post-service-upload-text and compose-post-service-upload-urls
    #  futures = []
    #  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        #  futures.append(executor.submit(upload_text, post_info, user_id, text, syscall))
        #  futures.append(executor.submit(upload_user_mentions, post_info, user_id, user_mentions, syscall))
        #  futures.append(executor.submit(upload_urls, post_info, user_id, user_mentions, syscall))

        #  # Results only give if functions are successfully invoked
        #  results = [f.result() for f in concurrent.futures.as_completed(futures)]

        #  if not all(results):
            #  return {"status":  "TextServiceUploadTextError",
                    #  "message": "Fail to invoke functions"}

        #  return {"status": "success"}

