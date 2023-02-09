class DagReader():
    def __init__(self, function):
        self.function = function
 
    def __call__(self, *args, **kwargs):
 
        # before function
        result = self.function(*args, **kwargs)
 
        # after function
        return result


# d = DagReader()

class Make():
    flow = []   
    nodes = set()
    def __init__(self,func) -> None:
        self.func = func
        Make.nodes.add(self.func.__name__)
    
    def __rshift__(self,next):
        Make.flow.append([self,next])
        return next

# @d.make
def add():
    pass

# @d.make
def sub():
    pass

# @d.make
def mul():
    pass

# @d.make
def div():
    pass


a = 4
b = 2
# print(f"{a} >> {b} = {a >> b}")

# def __rshift__(q,w):
#     flow.append(q)
#     flow.append(w)
#     def d():
#         pass
#     return d

# print(Make(add) >> Make(sub) >> Make(mul))
# print(Make(sub) >> Make(div))
