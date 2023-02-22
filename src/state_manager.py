import redis
import json
from config import STATE_MANAGER

class Redis():
    def __init__(self,host='127.0.0.1', port=6379,password=''):
        self.r = redis.Redis(
            host=host,
            port=port,
            password=password)
        self.r.ping()

    def push(self,key, val):
        try:
            if val is None:
                val = json.dumps({})
            self.r.set(key, json.dumps(val))
        except Exception:
            print("State not pushed, incompatible data")

    def pull(self,key):
        try:
            return {} if self.r.get(key) == b'' else json.loads(self.r.get(key))
        except Exception:
            print("State did not pulled, incompatible key")
            return {}


class StateManager():
    def __init__(self,manager = 'LOCAL'):
        if manager == 'LOCAL':
            pass
        if manager == 'REDIS':
            from config import REDIS_CON
            self.Mgr =  Redis(REDIS_CON["HOST"],REDIS_CON["PORT"],REDIS_CON["PASS"])

    def pull(self,key):
        return self.Mgr.pull(key)
        
    def push(self,key, val):
        return self.Mgr.push(key, val)

