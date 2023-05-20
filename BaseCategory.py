from collections import defaultdict

"""
Progress:
- Implement basic category and morphisms, where a category is an object `catA = Cat(A)`
- Change category code to superclass, now a category is any class `A(Category)` that extends `Category`
- Implement identity as a special morphism
- Add support for singleton category, use sets instead of lists for obC and morC
* Use factory method, do not mess with __new__()
* Use `Object` and `Morphism` classes, treat object and morphisms equally, seperate naming routines to a subclass
"""

class MorphismCategoryError(Exception):
    pass

class Object:
    def __init__(self, category: 'Category') -> None:
        self.category = category
        self.morphismsTo = defaultdict(set)
        self.morphismsFrom = defaultdict(set)
        self.identity = Morphism.construct(domain=self, codomain=self)


class Morphism:
    def __init__(self, domain: Object, codomain: Object) -> None:
        """Should not be called. Use factory `Morphism.construct()` instead."""
        if domain.category != codomain.category:
            raise MorphismCategoryError('domain and codomain must be objects within the same category')
        self.category = domain.category
        self.domain = domain
        self.codomain = codomain
    
    @classmethod
    def construct(cls, domain: Object, codomain: Object) -> 'Morphism':
        X, Y = domain, codomain
        newMorphism = Morphism(X, Y)
        X.morphismsTo[Y].add(newMorphism)
        Y.morphismsFrom[X].add(newMorphism)
        return newMorphism


class Category:
    def __init__(self, name: str) -> None:
        self.name = name
        self.objects = set()
        self.morphisms = set()
    
    def __repr__(self) -> str:
        return self.name
    
    def _newObject(self) -> Object:
        newObject = Object(category=self)
        self.objects.add(newObject)
        self.morphisms.add(newObject.identity)
        return newObject

    def _newMorphism(self, domain: Object, codomain: Object) -> Morphism:
        newMorphism = Morphism.construct(domain, codomain)
        self.morphisms.add(newMorphism)
        return newMorphism

    def someObject(self) -> Object:
        return self._newObject()

    def someMorphism(self, domain: Object, codomain: Object) -> Morphism:
        return self._newMorphism(domain, codomain)


if __name__ == '__main__':
    A = Category('A')
    A0 = A.someObject()
    A1 = A.someObject()
    id0 = A0.identity
    id1 = A1.identity
    f0 = A.someMorphism(A0, A0)
    f1 = A.someMorphism(A0, A1)
    f2 = A.someMorphism(A1, A1)
    newline = '\n\t'
    print(f"""
        {A =}
        {A0 =}
        {A1 =}
        {id0 =}
        {id1 =}
        {f0 =}
        {f1 =}
        {f2 =}
        {A.objects =}
        {A.morphisms =}
        A.morphisms
        {newline.join([str((m, m.domain, m.codomain, newline)) for m in A.morphisms])}
        A0.morphismsFrom[A0]
        {newline.join([str((m, m.domain, m.codomain, newline)) for m in A0.morphismsFrom[A0]])}
        A0.morphismsTo[A0]
        {newline.join([str((m, m.domain, m.codomain, newline)) for m in A0.morphismsTo[A0]])}
        A0.morphismsTo[A1]
        {newline.join([str((m, m.domain, m.codomain, newline)) for m in A0.morphismsTo[A1]])}
        A0.morphismsFrom[A1]
        {newline.join([str((m, m.domain, m.codomain, newline)) for m in A0.morphismsFrom[A1]])}
        A0.morphismsFrom[A0] == A0.morphismsTo[A0]: {A0.morphismsFrom[A0] == A0.morphismsTo[A0]}
        A0.morphismsTo[A1] == A1.morphismsFrom[A0]: {A0.morphismsTo[A1] == A1.morphismsFrom[A0]}
    """)