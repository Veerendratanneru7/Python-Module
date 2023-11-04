import io
import os
import sys
import logging
import time
from datetime import datetime

from put_content_to_s3 import put_content_to_s3

def get_string_io_logger(log_stringio_obj, logger_name):
	#create logger
	logger = logging.getLogger(logger_name)
	formatter = logging.Formatter("%(asctime)s %(levelname)s \t[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s")	
	logger.setLevel(logging.DEBUG)

	#add normal steam handler to display logs on screen
	io_log_handler = logging.StreamHandler()
	io_log_handler.setFormatter(formatter)
	logger.addHandler(io_log_handler)

	#create stream handler and initialise it with string io buffer
	string_io_log_handler = logging.StreamHandler(log_stringio_obj)
	string_io_log_handler.setFormatter(formatter)

	#add stream handler to logger
	logger.addHandler(string_io_log_handler)

	return logger

#create string i/o object as string buffer
log_stringio_obj = io.StringIO()

log_handler = logging.StreamHandler(log_stringio_obj)
logger = get_string_io_logger(log_stringio_obj, logger_name='my_s3_logger')
timestamp = datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
	s3_buck = "extensionlogs"
	s3_log_path = f"s3://{s3_buck}/python_logger/{timestamp}/"

	try:
		#do any task
		logger.info("Running my_function")
		logger.info("two")
		
	except Exception as e:
		exception_message = "message: {0}\nline no:{1}\n".format(str(e),sys.exc_info()[2].tb_lineno)
		logger.error(exception_message)
		
	finally:
		#persist logs in s3
		s3_store_response = put_content_to_s3(s3_path=s3_log_path+'logs.txt', content=log_stringio_obj.getvalue())
		assert s3_store_response['success'], "Error Putting logs to S3:\n{0}".format(s3_store_response['data'])