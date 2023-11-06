import os
import sys
import boto3

	
def put_content_to_s3(s3_path, content, s3_client=None, s3_resource=None, region_name='us-east-1', backup_key=None, backup_strategy='file'):
	return_object = {
		'success' : True,
		'data' : ''
	}
	try:
		bucket = s3_path.split('/')[2]
		key = '/'.join(s3_path.split('/')[3:])
		if not s3_client:
			s3_client_ = boto3.client('s3', region_name)
		else:
			s3_client_ = s3_client
		s3_put_response = s3_client_.put_object( Body=content, Bucket=bucket, Key=key )
		if s3_put_response['ResponseMetadata']['HTTPStatusCode']!=200:
			raise Exception('Unable to put data to s3: {0}'.format(s3_put_response))		
	except Exception as e:
		return_object['success'] = False
		exception_message = "message: {0}\nline no:{1}\n".format(str(e),sys.exc_info()[2].tb_lineno)
		return_object['data'] = exception_message
	finally:
		return return_object
