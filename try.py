from collections import defaultdict


class Parent:
    @classmethod
    def f(cls):
        try:
            cls.morphs
        except:
            cls.morphs = []
        print(cls.__name__)
        print(cls.f)
    


class Child(Parent):
    obs = []
    
    def __init__(self, play) -> None:
        super().__init__()
        self.play = play
    def bark(self):
        print('walf walf')

d = defaultdict(int, {1:2, 2:3})
print(d['hello'])
print(dict(d))