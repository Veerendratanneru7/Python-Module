import io
import os
import sys
import logging
import time
import boto3
import json
from datetime import datetime

TIMESTAMP = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H")
unix_epoch_timestamp = int(time.time())

def s3_path():
    s3_path = f"logs/{os.environ['APP_CAT_ID']}/{os.environ['SERVICE_NAME']}/{TIMESTAMP}/{os.environ['LAMBDA_NAME']}/{os.environ['CUSTOM_REQUEST_ID']}/{unix_epoch_timestamp}.log"
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

        # Construct the log entry using the custom JSON format
        time_stamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        s3_path_value = s3_path()
        corrId = s3_path_value.split('/')[-2]
        custom_log_format = {
            "functionName": os.environ.get('LAMBDA_NAME', 'UNKNOWN'),
            "corrId": corrId,
            "serviceName": os.environ.get('SERVICE_NAME', 'UNKNOWN'),
            "appCatId": os.environ.get('APP_CAT_ID', 'UNKNOWN'),
            "span_id": "undefined",
            "trace_id": "undefined",
            "logLevel": record.levelname,
            "detail": log_entry,
            "timestamp": time_stamp,
        }

        log_entry = json.dumps(custom_log_format)

        # Append the log entry to the existing content
        log_entry = existing_log_content + "\n" + log_entry

        # Upload the updated log content to S3
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=self.s3_bucket, Key=s3_path(), Body=log_entry)

def get_string_io_logger(log_stringio_obj, logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    io_log_handler = logging.StreamHandler()
    logger.addHandler(io_log_handler)

    # Add the custom S3 handler to automatically flush logs to S3
    s3_bucket = os.environ.get('S3_BUCKET')
    s3_handler = S3LogHandler(s3_bucket)
    logger.addHandler(s3_handler)
    return logger

log_stringio_obj = io.StringIO()
logger = get_string_io_logger(log_stringio_obj, "my_s3_logger")
timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
