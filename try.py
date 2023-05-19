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