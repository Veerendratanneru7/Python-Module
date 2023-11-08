import os
def request():
    request_id = os.environ.get('CUSTOM_REQUEST_ID')
    print(f"veeru: {request_id}")
    return request_id
