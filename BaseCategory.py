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

class MorphismCompositionError(Exception):
    pass

class Object:
    """
    Object {
        category: Category
        morphismsTo: map{codomain -> set(Morphisms)}
        morphismsFrom: map{domain -> set(Morphisms)}
        identity: Morphism
    }
    Tracked in following:
        some_morphism.domain: Object
        some_morphism.codomain: Object
        category.objects: set(Object)
    """
    def __init__(self, category: 'Category') -> None:
        self.category = category
        self.morphismsTo = defaultdict(set)
        self.morphismsFrom = defaultdict(set)
        self.identity = Morphism.construct(domain=self, codomain=self)


class Morphism:
    """
    Morphism {
        category: Category
        domain: Object
        codomain: Object
    }
    Tracked in following set(Morphisms):
        domain.morphismsTo[codomain]
        codomain.morphismsFrom[domain]
        category.morphisms
    """
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
        f = Morphism(X, Y)
        X.morphismsTo[Y].add(f)
        Y.morphismsFrom[X].add(f)
        f.category.morphisms.add(f)
        return f
    
    def makeEqualTo(self, another: Object):
        pass

    def composeWith(self, another: 'Morphism') -> 'Morphism':
        if self.codomain != another.domain:
            raise MorphismCompositionError('a.composedWith(b) must imply a.codomain == b.domain')
        return Morphism.construct(self.domain, another.codomain)

    def __matmul__(self, another):
        return self.composeWith(another)


class Category:
    """
    Category {
        name: str
        objects: set{Object}
        morphisms: set{Morphism}
    }
    """
    def __init__(self, name: str = None) -> None:
        self.name = name if name else object.__repr__(self)
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
        return newMorphism

    def someObject(self) -> Object:
        return self._newObject()

    def someMorphism(self, domain: Object, codomain: Object) -> Morphism:
        return self._newMorphism(domain, codomain)


if __name__ == '__main__':
    A = Category()
    A0 = A.someObject()
    A1 = A.someObject()
    A2 = A.someObject()
    id0 = A0.identity
    id1 = A1.identity
    id2 = A2.identity
    f0 = A.someMorphism(A0, A0)
    f1 = A.someMorphism(A0, A1)
    f2 = A.someMorphism(A1, A2)
    g = f1 @ f2
    mapinfo = lambda f: str((f, f.domain, f.codomain))
    newline = '\n\t\t'
    print(f"""
        {A   = }
        {A0  = }
        {A1  = }
        {A2  = }
        {id0 = }
        {id1 = }
        {id2 = }
        {f0  = }
        {f1  = }
        {f2  = }
        A.objects
                {newline.join([str(ob) for ob in A.objects])}
        A.morphisms
                {newline.join([mapinfo(m) for m in A.morphisms])}
        A0.morphismsFrom[A0]
                {newline.join([mapinfo(m) for m in A0.morphismsFrom[A0]])}
        A0.morphismsTo[A0]
                {newline.join([mapinfo(m) for m in A0.morphismsTo[A0]])}
        A0.morphismsTo[A1]
                {newline.join([mapinfo(m) for m in A0.morphismsTo[A1]])}
        A0.morphismsFrom[A1]
                {newline.join([mapinfo(m) for m in A0.morphismsFrom[A1]])}
        {A0.morphismsFrom[A0] == A0.morphismsTo[A0] = }
        {A0.morphismsTo[A1] == A1.morphismsFrom[A0] = }
        {mapinfo(g) = }
    """)