from config import *
from minio import Minio
from minio.error import S3Error
import traceback, os

class BucketOPS:
    def __init__(self,bucket_type):
        self.type = bucket_type
        self.get_client()

    def get_client(self):
        if self.type == "MINIO":
            client = Minio(
                "minio:9000",
                access_key="c@rpl@c@ring",
                secret_key="c@rpl@c@ring",
                secure=False,
            )
        else:
            pass
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
            self.client.fget_object(
                bucket_name,
                object_name,
                file_name
            )
            print("File downloaded successfully!")
        except Exception:
            print(traceback.format_exc())

class Connection():
    def __init__(self):
        if FETCH_FLOWS:
            if FETCH_FLOWS_FROM == 'MINIO':
                self.con = BucketOPS('MINIO')
            
            if FETCH_FLOWS_FROM == 'S3':
                self.con = BucketOPS('S3')

        else:
            pass
            