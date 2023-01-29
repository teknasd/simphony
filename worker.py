#!/usr/bin/env python
import sys, os
from rabi import Rabi
from pprint import pprint
import json
import funcs

def callback(ch, method, properties, body):
    print("---------- recieved ---------")
    pprint(ch.__dict__)
    print(" [x] Received %r" % body)
    fun = json.loads(body)
    print(fun)
    print("---------- start ------------")

    module = __import__(fun['dag'])
    bar = getattr(module, fun['call'])
    bar()


def main():
    r = Rabi(q = "ex")
    r.listen_and_call(call= callback)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)