import io
import os
import sys
import logging
import time
import boto3
from datetime import datetime

from put_content_to_s3 import put_content_to_s3
from put_content_to_s3 import get_content_from_s3

class S3LogHandler(logging.Handler):
    def __init__(self, s3_bucket, s3_prefix):
        super().__init__()
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix
        self.log_file = None  # Initialize log_file to None

    def open_log_file(self):
        timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
        lambda_request_id = context.aws_request_id if 'context' in globals() else 'unknown_request_id'
        self.log_file = f"s3://{self.s3_bucket}/{self.s3_prefix}/{timestamp}/{lambda_request_id}/logs.txt"
        get_content_from_s3(self.log_file)

    def emit(self, record):
        if self.log_file is None:
            self.open_log_file()

        log_entry = self.format(record)
        put_content_to_s3(self.log_file, log_entry, append=True)  # Append log entry
        
def get_string_io_logger(log_stringio_obj, logger_name, s3_bucket, s3_prefix):
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
    s3_handler = S3LogHandler(s3_bucket, s3_prefix)
    s3_handler.setFormatter(formatter)
    logger.addHandler(s3_handler) 
    return logger

log_stringio_obj = io.StringIO()
logger = get_string_io_logger(log_stringio_obj, "my_s3_logger", "extensionlogs", "python-lambda")
timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")