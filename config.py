
# ---------------------------------------------------------
#  state settings
''' set redis connection '''
STATE_MANAGER = 'REDIS'
REDIS_CON = {
    "HOST" : '127.0.0.1',
    "PORT" : 6379,
    "PASS" : ''
}

# ---------------------------------------------------------
# rabbit settings
''' set rabbit connection '''
RABBIT_CON = {
    "LOCATION" : "172.16.12.17",
    "PORT" : 5672
}

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
