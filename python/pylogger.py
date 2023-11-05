import io
import os
import sys
import logging
import time
from datetime import datetime
from put_content_to_s3 import put_content_to_s3

# Configuration for automatic log uploading
AUTOMATIC_LOG_UPLOAD = True  # Set this to True to enable automatic log uploading

# Initialize string i/o object as a string buffer
log_stringio_obj = io.StringIO()
log_handler = logging.StreamHandler(log_stringio_obj)
logger = logging.getLogger("my_s3_logger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s \t[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

if AUTOMATIC_LOG_UPLOAD:
    # Automatically upload logs to S3 after each log event
    def upload_logs_to_s3(log_record):
        timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
        s3_bucket = "extensionlogs"
        s3_log_path = f"s3://{s3_bucket}/python-lambda/{timestamp}/logs.txt"
        put_content_to_s3(s3_log_path, log_record.getMessage())

    # Create a custom log handler that triggers log uploads
    class S3LogHandler(logging.StreamHandler):
        def emit(self, record):
            log_message = self.format(record)
            upload_logs_to_s3(log_message)

    s3_log_handler = S3LogHandler()
    s3_log_handler.setFormatter(formatter)
    logger.addHandler(s3_log_handler)
