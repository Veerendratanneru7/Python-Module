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
        request_id = record.request_id if hasattr(record, 'request_id') else 'unknown'
        try:
            response = s3_client.get_object(Bucket=self.s3_bucket, Key=self.s3_prefix)
            existing_log_content = response['Body'].read().decode('utf-8')
        except s3_client.exceptions.NoSuchKey:
            existing_log_content = ""

        # Append the log entry to the existing content
        log_entry = existing_log_content + log_entry

        # Upload the updated log content to S3
        s3_client.put_object(Bucket=self.s3_bucket, Key=self.s3_prefix, Body=log_entry)


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
    return logger

log_stringio_obj = io.StringIO()
logger = get_string_io_logger(log_stringio_obj, "my_s3_logger")
timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
