x = y = 3
print(x, y)

class Parent:
    @classmethod
    def f(cls):
        try:
            cls.morphs
        except:
            cls.morphs = []
    


class Child(Parent):
    obs = []
    pass

print(hasattr(Child(), 'obs'))

class A:
    pass

def f():
    if f.obj is None:
        f.obj = A()
    return f.obj

f.obj = None