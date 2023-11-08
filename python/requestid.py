import os

def capture_request_id(context):
    request_id = context.aws_request_id
    os.environ['REQUEST_ID'] = request_id

# Automatically capture the request ID when the layer is loaded
import boto3
lambda_client = boto3.client('lambda')
this_lambda_arn = os.environ['AWS_LAMBDA_FUNCTION_NAME']
this_lambda_response = lambda_client.get_function(
    FunctionName=this_lambda_arn,
)
this_lambda_context = this_lambda_response['Configuration']['FunctionArn']
capture_request_id(this_lambda_context)
