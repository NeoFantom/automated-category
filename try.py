# class A:
#     def __init__(self):
#         print(self.__class__.__name__)

#     def f(x):
#         if type(x) == int:
#             print(x+1)
#         elif type(x) == float:
#             print(x / 2)

# class A1(A):
#     def __init__(self):
#         self.super.__init__()

#     def f(x):
#         print(x, 'is in A1')


class Father:

    def __init__(self):
        def _serialName(cls, obj):
            obj.name = f'{cls.__name__}{len(cls.objects)}'
            cls.objects.append(obj)
        self.__class__.objects.append(1)
        print(f'{self.__class__=}')
        _serialName(self.__class__, self)

    def __repr__(self):
        return self.name


class Child(Father):
    objects = []

    def __init__(self):
        Father.__init__(self)


c = Child()
print(c)
print(type(c))
print(c.name)
