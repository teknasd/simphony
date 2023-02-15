import redis
import json
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    password='')


def push(key, val):
    if val is None:
        val = json.dumps({})
    r.set(key, json.dumps(val))


def pull(key):
    return {} if r.get(key) == b'' else json.loads(r.get(key))