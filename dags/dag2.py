import numpy as np
import time
from rshift import *
from time import sleep


def qwe(context):
    print(f"context: {context}")
    context["a"] = 2
    sleep(3)
    return context


def uyiui(context):
    print(f"context: {context}")
    context["b"] = context["a"] ** 3
    sleep(3)
    return context


def bbvkj(context):
    print(f"context: {context}")
    context["c"] = context["b"] ** 5
    sleep(3)
    return context


Make(qwe) >> Make(uyiui) >> Make(bbvkj)