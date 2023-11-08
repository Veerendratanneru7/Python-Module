import io
import os
import sys
import logging
import time
import boto3
from datetime import datetime
from put_content_to_s3 import put_content_to_s3

class S3LogHandler(logging.Handler):
    def __init__(self, s3_bucket, s3_prefix):
        super().__init__()
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix

    def emit(self, record):
        log_entry = self.format(record)
        #timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
        s3_log_path = f"s3://{self.s3_bucket}/{self.s3_prefix}"
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
    TIMESTAMP = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H")
    unix_epoch_timestamp = int(time.time())

    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=os.environ['S3_BUCKET'], Key=f'request-ids/id.txt')
    object_content = response['Body'].read().decode('utf-8')
    print(object_content)

    s3_prefix = f"logs/{os.environ['APP_CAT_ID']}/{os.environ['FUNCTION_NAME']}/{TIMESTAMP}/{os.environ['LAMBDA_NAME']}/1/{unix_epoch_timestamp}.log"
    print(s3_prefix)

    s3_handler = S3LogHandler(s3_bucket, s3_prefix)
    s3_handler.setFormatter(formatter)
    logger.addHandler(s3_handler)

    return logger

log_stringio_obj = io.StringIO()
logger = get_string_io_logger(log_stringio_obj, "my_s3_logger")
timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
