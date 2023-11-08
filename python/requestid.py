import boto3
import os

def capture_request_id(context):
    request_id = context.aws_request_id
    s3_client = boto3.client('s3')
    response = s3_client.put_object(Bucket=os.environ['S3_BUCKET'], Key=f'request-ids/id.txt', Body=request_id)
    print(request_id)
    print(response)
    return request_id
