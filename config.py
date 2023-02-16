''' task retries on faliure '''
TASK_RETRY_COUNT = 3


#  state settings
''' '''
STATE_MANAGER = 'REDIS'
REDIS_CON = {
    "HOST" : '127.0.0.1',
    "PORT" : 6379,
    "PASS" : ''
}

# rabbit settings
''' location '''
RABBIT_CON = {
    "LOCATION" : "172.16.12.17",
    "PORT" : 5672
}

''' '''
EX_Q = 'ex'

''' '''
ACK_Q = 'ack'


