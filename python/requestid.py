import boto3
import os

def capture_request_id(context):
    request_id = context.aws_request_id
    s3_client = boto3.client('s3')
    request_id_bytes = request_id.encode('utf-8')
    s3_client.put_object(Bucket=os.environ['S3_BUCKET'], Key=f'request-ids/{request_id}.txt', Body=request_id_bytes)
    return request_id

