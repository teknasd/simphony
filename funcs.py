import numpy as np
import time
from rshift import *
def a():
    print("inside func a")
    time.sleep(5)

def b():
    for i in range(10):
        print(i)
    time.sleep(5)
    # raise "Eroor in BBBBBBBBBB"

def c():
    for i in range(10,0,-1):
        print(i)
    time.sleep(5)

def d():
    pass

def e():
    pass


Make(a) >> Make(b) >> Make(d)
Make(a) >> Make(c) >> Make(e)


def mad():
    print("insidde multiverse")
# print(flow)
# for f in flow:
#     for t in f:
#         print(t.func)

Make(mad)