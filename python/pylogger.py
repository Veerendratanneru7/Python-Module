import io
import os
import sys
import logging
import time
from datetime import datetime

from put_content_to_s3 import put_content_to_s3


def get_string_io_logger(log_stringio_obj, logger_name):
    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # add normal steam handler to display logs on screen
    io_log_handler = logging.StreamHandler()
    logger.addHandler(io_log_handler)

    # create stream handler and initialise it with string io buffer
    string_io_log_handler = logging.StreamHandler(log_stringio_obj)

    # add stream handler to logger
    logger.addHandler(string_io_log_handler)

    #return logger


def get_logs(log_stringio_obj):
    timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
    s3_buck = "extensionlogs"
    s3_log_path = f"s3://{s3_buck}/python-lambda/{timestamp}/"
    s3_store_response = put_content_to_s3(
        s3_path=s3_log_path + "logs.txt", content=log_stringio_obj.getvalue()
    )
    return log_stringio_obj.getvalue()
    

# create string i/o object as string buffer
log_stringio_obj = io.StringIO()
log_handler = logging.StreamHandler(log_stringio_obj)
logger = get_string_io_logger(log_stringio_obj, logger_name="my_s3_logger")
timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
