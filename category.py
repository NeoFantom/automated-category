from typing import Any

class MorphismDomainError(Exception):
    pass

class MorphismCategoryError(Exception):
    pass

class MorphismUndefinedError(Exception):
    pass

class Morphism:

    def __init__(self, category, domain, codomain):
        """
        - `domain` and `codomain` must be instances `category`
        - `category` msut be a subclass of `Category`
        """
        if type(domain) == category and type(codomain) == category:
            self.category = category
            try:
                category.morphisms.append(self)
            except AttributeError:
                category.morphisms = [self]
            self.name = f'{category.__name__}_mor{len(category.morphisms)}'
            self.domain = domain
            self.codomain = codomain
            x, y = domain, codomain
            def addSelf(d: dict, v):
                try:
                    d[v].add(self)
                except KeyError:
                    d[v] = {self}
            addSelf(x.morphismsTo, y)
            addSelf(y.morphismsFrom, x)
        else:
            raise MorphismCategoryError(
                f"Morphism's domain & codomain must be instances of the category {category.name}")
        return
    
    def __repr__(self) -> str:
        return f'{self.name}: {self.domain} -> {self.codomain} @{object.__repr__(self)}'

class Category:
    def __init__(self):
        self.morphismsTo = {}
        self.morphismsFrom = {}

    @classmethod
    def anyObject(cls):
        newObject = cls()

        category = cls
        try:
            category.objects.append(newObject)
        except AttributeError:
            category.objects = [newObject]
        return newObject

    @classmethod    
    def anyMorphism(cls, domain, codomain) -> Morphism:
        morphism = Morphism(category=cls, domain=domain, codomain=codomain)
        return morphism

class SerialNamedType:

    def __init__(self):
        cls = self.__class__
        try:
            objects = cls.namedObjects
        except AttributeError:
            objects = cls.namedObjects = []
        self.name = f'{cls.__name__}{len(objects)}'
        objects.append(self)

        # def _serialName(cls, obj):  
        #     obj.name = f'{cls.__name__}{len(cls.objects)}'
        #     cls.objects.append(obj)
        # _serialName(self.__class__, self)
       
    def __repr__(self):
        return self.name

class A(Category, SerialNamedType):
    def __init__(self):
        Category.__init__(self)
        SerialNamedType.__init__(self)

class B(Category, SerialNamedType):
    def __init__(self):
        Category.__init__(self)
        SerialNamedType.__init__(self)

def try_execute(f, x):
    try:
        return f(x)
    except Exception as e:
        print(e)

a0 = A.anyObject()
a1 = A.anyObject()
f = A.anyMorphism(a0, a1)
g = A.anyMorphism(a0, a1)
print(a0, a1, f, g, sep='\n')

# catA = CategoryOf(A)
# a1 = catA.anyObject()
# a2 = catA.anyObject()
# a3 = catA.anyObject()
# catB = CategoryOf(B)
# b1 = catB.anyObject()
# f_a1_a2 = catA.anyMorphism(domain=a1, codomain=a2)
# print(a1, a2, a3, b1)
# print(A.objects, B.objects)
# print()

# print(try_execute(f_a1_a2, a1) == a2)
# print(try_execute(f_a1_a2, a2) == a2)
# print(try_execute(f_a1_a2, a3) == a2)
# print(try_execute(f_a1_a2, b1) == a2)