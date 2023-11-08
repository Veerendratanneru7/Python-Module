import os
def request():
    request_id = os.environ.get('CUSTOM_REQUEST_ID')
    if request_id:
        print(f"Request ID: {request_id}")
    else:
        print("REQUEST_ID environment variable not found.")
    return request_id
