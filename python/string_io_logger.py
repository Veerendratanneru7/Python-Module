import io
import logging
import sys
import time
from datetime import datetime

from put_content_to_s3 import put_content_to_s3


def get_string_io_logger(log_stringio_obj, logger_name):
    # Create logger
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s \t[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
    )
    logger.setLevel(logging.DEBUG)

    # Add a stream handler to display logs on the console
    console_log_handler = logging.StreamHandler()
    console_log_handler.setFormatter(formatter)
    logger.addHandler(console_log_handler)

    # Create a stream handler and initialize it with the log_stringio_obj buffer
    string_io_log_handler = logging.StreamHandler(log_stringio_obj)
    string_io_log_handler.setFormatter(formatter)

    # Add the string_io_log_handler to the logger
    logger.addHandler(string_io_log_handler)

    return logger


def store_logs_in_s3(log_stringio_obj):
    timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
    s3_buck = "extensionlogs"
    s3_log_path = f"s3://{s3_buck}/python-lambda/{timestamp}/"
    s3_store_response = put_content_to_s3(
        s3_path=s3_log_path + "logs.txt", content=log_stringio_obj.getvalue()
    )
    return log_stringio_obj.getvalue()

    # Create a StringIO object as a string buffer
log_stringio_obj = io.StringIO()
log_handler = logging.StreamHandler(log_stringio_obj)
logger = get_string_io_logger(log_stringio_obj, logger_name="my_s3_logger")
