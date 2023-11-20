import boto3
from botocore.exceptions import ClientError
from boto3 import logging
import sys

class BucketWrapper:
    def __init__(self, s3_bucket) -> None:
        self.bucket = s3_bucket
        self.name = s3_bucket.name
        #self.logger = logging.getLogger()


    def get_objects(self, client):
        try:
            response = client.list_objects_v2(Bucket=self.name)
            objects = []
            objects = list(o['Key'] for o in response['Contents'])
            logging.info('Got objects: %s', objects)
            
        except ClientError:
            logging.exception('Could not get objects')
            raise
        except  KeyError:
            logging.exception('Contents are empty')
        else:
            return objects
        
    def get_object(self, client, object_id):
        pass

    def add_object(self, client, file_name, object_id) -> bool:        
        s3_client = client
        try:
            response = s3_client.upload_file(file_name, self.name, object_id)
            logging.log(f'Uploaded file {response}')
        except ClientError:
            logging.exception('Could not upload file.')
            return False
        else:
            return True


