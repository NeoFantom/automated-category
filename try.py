from collections import defaultdict


class Parent:
    def f(self):
        pass

    def g(self):
        self.f()
    


class Child(Parent):
    def f(self, name):
        print(name, 'is received')
    


c = Child()
x = 3
x += 4 + 9
print(x)

if set():
    print('if')
else:
    print('else')
