import io
import os
import sys
import logging
import time
import boto3
from datetime import datetime
from put_content_to_s3 import put_content_to_s3

def capture_request_id(context):
    request_id = context.aws_request_id
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=os.environ['S3_BUCKET'], Key=f'request-ids/{request_id}.txt', Body=request_id)
    os.environ['REQUEST_ID'] = request_id
    return request_id

class structure(logging.Handler)    
    def s3_log_structure():
        TIMESTAMP = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H")
        unix_epoch_timestamp = int(time.time())
        #log_path = f"logs/os.environ['APP_CAT_ID']/os.environ['FUNCTION_NAME']/{TIMESTAMP}/os.environ['LAMBDA_NAME']/{request_id}/{unix_epoch_timestamp}.log"
        log_path = f"logs/os.environ['APP_CAT_ID']/os.environ['FUNCTION_NAME']/{TIMESTAMP}/os.environ['LAMBDA_NAME']/1/{unix_epoch_timestamp}.log"
        print(log_path)


class S3LogHandler(logging.Handler):
    def __init__(self, s3_bucket, s3_prefix):
        super().__init__()
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix

    def emit(self, record):
        log_entry = self.format(record)
        #timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
        s3_log_path = f"s3://{self.s3_bucket}/{self.s3_prefix}/logs.txt"
        put_content_to_s3(s3_log_path, log_entry)

def get_string_io_logger(log_stringio_obj, logger_name):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s \t[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
    )
    logger.setLevel(logging.DEBUG)

    io_log_handler = logging.StreamHandler()
    io_log_handler.setFormatter(formatter)
    logger.addHandler(io_log_handler)

    string_io_log_handler = logging.StreamHandler(log_stringio_obj)
    string_io_log_handler.setFormatter(formatter)
    logger.addHandler(string_io_log_handler)

    # Add the custom S3 handler to automatically flush logs to S3
    s3_bucket = os.environ.get('S3_BUCKET')
    s3_prefix = os.environ.get('LOG_FILE_NAME')
    s3_handler = S3LogHandler(s3_bucket, s3_prefix)
    s3_handler.setFormatter(formatter)
    logger.addHandler(s3_handler)
    s3structure = structure()
    logger.addHandler(s3structure)
    return logger

log_stringio_obj = io.StringIO()
logger = get_string_io_logger(log_stringio_obj, "my_s3_logger")
timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
