import numpy as np
import time
from rshift import *


def qwe(context):
    print(f"context: {context}")
    context["a"] = 2
    return context


def uyiui(context):
    print(f"context: {context}")
    context["b"] = context["a"] ** 2
    return context


def bbvkj(context):
    print(f"context: {context}")
    context["c"] = context["b"] ** 2
    return context


Make(qwe) >> Make(uyiui) >> Make(bbvkj)