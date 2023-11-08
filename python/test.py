import os
def request():
    request_id = os.environ.get('CUSTOM_REQUEST_ID')
    print(f"Request ID: {request_id}")
    return request_id
