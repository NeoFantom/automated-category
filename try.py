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
    pass

# print(Child.morphs)
print(Child.f())
print(Child.morphs)