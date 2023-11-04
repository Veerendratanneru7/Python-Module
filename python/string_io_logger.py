import io
import logging
import os
import sys
import time
from datetime import datetime

from put_content_to_s3 import put_content_to_s3


def get_string_io_logger(log_stringio_obj, logger_name):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s \t[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
    )
    logger.setLevel(logging.DEBUG)

    # add normal steam handler to display logs on screen
    io_log_handler = logging.StreamHandler()
    io_log_handler.setFormatter(formatter)
    logger.addHandler(io_log_handler)

    # create stream handler and initialise it with string io buffer
    string_io_log_handler = logging.StreamHandler(log_stringio_obj)
    string_io_log_handler.setFormatter(formatter)

    # add stream handler to logger
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
