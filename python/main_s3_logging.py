import io
import sys
import logging
import time
from datetime import datetime

from put_content_to_s3 import put_content_to_s3
from string_io_logger import get_string_io_logger

def my_function():
	#create string i/o object as string buffer
	log_stringio_obj = io.StringIO()

	#create stream log handler with string i/o buffer
	log_handler = logging.StreamHandler(log_stringio_obj)
	logger = get_string_io_logger(log_stringio_obj, logger_name='my_s3_logger')
	
	#s3 log path
	timestamp = datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
	s3_buck = os.environ.get('S3_BUCKET')
	s3_log_path = f"s3://{s3_buck}/python_s3_logger_demo/{timestamp}/"

	try:
		#do any task
		logger.info("Running my_function")
		
	except Exception as e:
		exception_message = "message: {0}\nline no:{1}\n".format(str(e),sys.exc_info()[2].tb_lineno)
		logger.error(exception_message)
		
	finally:
		#persist logs in s3
		s3_store_response = put_content_to_s3(s3_path=s3_log_path+'logs.txt', content=log_stringio_obj.getvalue())
		assert s3_store_response['success'], "Error Putting logs to S3:\n{0}".format(s3_store_response['data'])
