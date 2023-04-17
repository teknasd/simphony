from config import *
from minio import Minio
from minio.error import S3Error
import traceback, os


class BaseClass:
    def __init__(self):
        self.type = bucket_type
   
    def get_object(self,bucket_name = "",object_name = "",file_name = ""):
        return False

class BucketOPS(BaseClass):
    def __init__(self,bucket_type):
        self.type = bucket_type
        self.get_client()

    def get_client(self):
        if self.type == "MINIO":
            client = Minio(
                MINIO_ENDPOINT,
                access_key=MINIO_ACCESS_KEY,
                secret_key=MINIO_SECRET_KEY,
                secure=False,
            )
        elif self.type == "S3":
            session = boto3.session.Session()
            client = session.client(
                service_name='s3',
                aws_access_key_id=S3_ACCESS_KEY,
                aws_secret_access_key=S3_SECRET_KEY,
                config=Config(signature_version='s3v4', s3={'addressing_style': 'path'},
                retries = {
                    'max_attempts': 10,
                    'mode': 'standard'
                }
                ),
                region_name=S3_REGION
                )
        self.client = client
        return client
    
    def put_object(self,bucket_name = "",object_name = "",object_data = None):
        if self.type == "MINIO":
            try:
                with open(object_data, "rb") as file_data:
                    file_stat = os.stat(object_data)
                    self.client.put_object(
                        bucket_name,
                        object_name,
                        file_data,
                        file_stat.st_size,
                    )
                print("File uploaded successfully")
                return True
            except S3Error as e:
                print(traceback.format_exc())
                return False
        else:
            return False


    def get_object(self,bucket_name = "",object_name = "",file_name = ""):
        try:
            if self.type == "MINIO":
                self.client.fget_object(
                    bucket_name,
                    object_name,
                    file_name
                )
                print("File downloaded successfully!")
                return True

                # Upload the file
            elif self.type == "S3":
                response = self.client.download_file(bucket_name, object_name, file_name)
                print(response)
                return True

        except Exception:
            print(traceback.format_exc())
            return False

class Connection():
    def __init__(self):
        print("FETCH_FLOWS",FETCH_FLOWS)
        print("FETCH_FLOWS_FROM",FETCH_FLOWS_FROM)
        if FETCH_FLOWS:
            if FETCH_FLOWS_FROM == 'MINIO':
                self.con = BucketOPS('MINIO')
            elif FETCH_FLOWS_FROM == 'S3':
                self.con = BucketOPS('S3')
            else:
                self.con = BaseClass()
        else:
            pass
            self.con = None
