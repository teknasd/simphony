import os
from dotenv import load_dotenv
import redis
import datetime,base64
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env.dev'))

# ---------------------------------------------------------
#  state settings
''' set redis connection '''
STATE_MANAGER = os.environ.get('STATE_MANAGER')
REDIS_CON = {
    "HOST" : os.environ.get('REDIS_CON_IP'),
    "PORT" : os.environ.get('REDIS_CON_PORT'),
    "PASS" : ''
}

# ---------------------------------------------------------
# rabbit settings
''' set rabbit connection '''
RABBIT_CON = {
    "LOCATION" : os.environ.get('RABBIT_CON_IP'),
    "PORT" : os.environ.get('RABBIT_CON_PORT')
}

''' set ackowledge queue '''
CALL_Q = 'ack'

''' set execution queue '''
EX_Q = 'ex'

''' set ackowledge queue '''
ACK_Q = 'ack'

# ---------------------------------------------------------
# dags
''' set dag folder '''
DAG_FOLDER = 'dags'


# ---------------------------------------------------------
# task setting
''' set task retries on faliure '''
TASK_RETRY_COUNT = 3


# ---------------------------------------------------------
#  Concurrency settings (threads)
''' set the number of threads in a worker '''
CONCURRENCY = 1


# --------------------------------------------------------
#  Fetch Flows
FETCH_FLOWS = True
FETCH_FLOWS_FROM = 'MINIO'

# --------------------------------------------------------
#  Fetch Flows - Minio
MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
MINIO_SECURE = os.environ.get('MINIO_SECURE')
MINIO_BUCKET = os.environ.get('MINIO_BUCKET')

# --------------------------------------------------------
#  Fetch Flows - S3
S3_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
S3_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
S3_REGION = os.environ.get('AWS_REGION')
S3_BUCKET = os.environ.get('AWS_BUCKET')
