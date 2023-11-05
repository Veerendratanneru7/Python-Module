import io
import os
import sys
import logging
import time
from datetime import datetime
from put_content_to_s3 import put_content_to_s3

# Create a string i/o object as a string buffer
log_stringio_obj = io.StringIO()

# Create the logger
logger = logging.getLogger("my_s3_logger")
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s \t[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
)
logger.setLevel(logging.DEBUG)

# Add a normal stream handler to display logs on the screen
io_log_handler = logging.StreamHandler()
io_log_handler.setFormatter(formatter)
logger.addHandler(io_log_handler)

# Create a stream handler and initialize it with the string io buffer
string_io_log_handler = logging.StreamHandler(log_stringio_obj)
string_io_log_handler.setFormatter(formatter)

# Add the stream handler to the logger
logger.addHandler(string_io_log_handler)

# Set up S3 upload settings
timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
s3_bucket = "extensionlogs"
s3_log_path = f"s3://{s3_bucket}/python-lambda/{timestamp}/"

# Function to automatically upload logs to S3
def upload_logs_to_s3():
    s3_store_response = put_content_to_s3(
        s3_path=s3_log_path + "logs.txt", content=log_stringio_obj.getvalue()
    )

# Define a cleanup function to upload logs when the Lambda function exits
def cleanup():
    upload_logs_to_s3()

# Import the `atexit` module if available
try:
    import atexit
    atexit.register(cleanup)
except ImportError:
    pass
