from pprint import pprint
import send, recieve
class C():
    '''
    this is a class
    '''
    def __init__(self) -> None:
        self.a = 1
        self.b = 2
        self.c = 3

    def get(self):
        pass

    def set(self):
        pass

    def delete(self):
        pass


obj = C()
pprint(dir(obj))
pprint(globals())