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

c = Parent()
c.__class__ = Child
c.bark()
c.__init__(23)
print(c.play)