from typing import Any

class MorphismDomainError(Exception):
    pass

class MorphismUndefinedError(Exception):
    pass

class Morphism:
    def __init__(self, theCat, domain, codomain, action=None):
        self.theCat = theCat
        self.domain = domain
        self.codomain = codomain
        self.action = action
    
    def __call__(self, x):
        if type(x) != self.domain:
            raise MorphismDomainError(f'input {x} is not in the domain of this morphism')
        elif self.action is None:
            raise MorphismUndefinedError(f'Morphism action on elements is not defined.')
        else:
            return self.action(x)

class CategoryOf:
    def __init__(self, theCat):
        self.theCat = theCat
        self.objects = []
        self.morphismsFrom = {}
        self.morphismsTo = {}

    def anyObject(self):
        ob = self.theCat()
        self.objects.append(ob)
        self.morphismsFrom[ob] = []
        self.morphismsTo[ob] = []
        return ob
    
    def anyMorphism(self, domain, codomain) -> Morphism:
        morphism = Morphism(self.theCat, domain, codomain)
        self.morphismsFrom[domain].append(morphism)
        self.morphismsTo[codomain].append(morphism)
        return morphism

class SerialNamedType:

    def __init__(self):
        def _serialName(cls, obj):  
            obj.name = f'{cls.__name__}{len(cls.objects)}'
            cls.objects.append(obj)
        _serialName(self.__class__, self)
       
    def __repr__(self):
        return self.name

class A(SerialNamedType):
    objects = []
    def __init__(self):
        SerialNamedType.__init__(self)

class B(SerialNamedType):
    objects = []
    def __init__(self):
        SerialNamedType.__init__(self)

def try_execute(f, x):
    try:
        return f(x)
    except Exception as e:
        print(e)

catA = CategoryOf(A)
a1 = catA.anyObject()
a2 = catA.anyObject()
a3 = catA.anyObject()
catB = CategoryOf(B)
b1 = catB.anyObject()
f_a1_a2 = catA.anyMorphism(domain=a1, codomain=a2)
print(a1, a2, a3, b1)
print(A.objects, B.objects)
print()

print(try_execute(f_a1_a2, a1) == a2)
print(try_execute(f_a1_a2, a2) == a2)
print(try_execute(f_a1_a2, a3) == a2)
print(try_execute(f_a1_a2, b1) == a2)