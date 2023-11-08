import io
import os
import sys
import logging
import time
import boto3
from datetime import datetime

def s3_path():
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=os.environ['S3_BUCKET'], Key=f'request-ids/id.txt')
    object_content = response['Body'].read().decode('utf-8')
    TIMESTAMP = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H")
    unix_epoch_timestamp = int(time.time())
    s3_path = f"logs/{os.environ['APP_CAT_ID']}/{os.environ['FUNCTION_NAME']}/{TIMESTAMP}/{os.environ['LAMBDA_NAME']}/{object_content}/{unix_epoch_timestamp}.log"
    print(s3_path)
    return s3_path

class S3LogHandler(logging.Handler):
    def __init__(self, s3_bucket):
        super().__init__()
        self.s3_bucket = s3_bucket

    def emit(self, record):
        log_entry = self.format(record)
        request_id = getattr(record, 'request_id', 'unknown')
        try:
            s3_client = boto3.client('s3')
            response = s3_client.get_object(Bucket=self.s3_bucket, Key=s3_path())
            existing_log_content = response['Body'].read().decode('utf-8')
        except s3_client.exceptions.NoSuchKey:
            existing_log_content = ""

        # Append the log entry to the existing content
        log_entry = existing_log_content + log_entry

        # Upload the updated log content to S3
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=self.s3_bucket, Key=s3_path(), Body=log_entry)


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
    s3_handler = S3LogHandler(s3_bucket)
    s3_handler.setFormatter(formatter)
    logger.addHandler(s3_handler)
    return logger

log_stringio_obj = io.StringIO()
logger = get_string_io_logger(log_stringio_obj, "my_s3_logger")
timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
