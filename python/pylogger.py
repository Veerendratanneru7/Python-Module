import io
import os
import sys
import logging
import time
from datetime import datetime

from put_content_to_s3 import put_content_to_s3

class S3LogHandler(logging.Handler):
    def __init__(self, s3_bucket, s3_prefix):
        super().__init__()
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix
        self.log_entries = []
        self.log_file = None

    def emit(self, record):
        log_entry = self.format(record)
        self.log_entries.append(log_entry)

    def close(self):
        if self.log_entries:
            log_content = '\n'.join(self.log_entries)
            self.open_log_file()
            put_content_to_s3(self.log_file, log_content)

    def open_log_file(self):
        if self.log_file is None:
            self.log_file = f"s3://{self.s3_bucket}/{self.s3_prefix}/logs.txt"
        
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
logger = get_string_io_logger(log_stringio_obj, "my_s3_logger", "extensionlogs", "python-veeru")
timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
