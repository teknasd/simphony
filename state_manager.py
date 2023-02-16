import redis
import json
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    password='')



def push(key, val):
    try:
        if val is None:
            val = json.dumps({})
        r.set(key, json.dumps(val))
    except Exception:
        print("State not pushed, incompatible data")


def pull(key):
    try:
        return {} if r.get(key) == b'' else json.loads(r.get(key))
    except Exception:
        print("State did not pulled, incompatible key")
        return {}