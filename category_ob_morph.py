from typing import Any
import itertools
from collections import defaultdict

from category_ob_morph import Morphism, Object

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
    def construct(cls, domain: Object, codomain: Object) -> Morphism:
        x, y = domain, codomain
        newMorphism = Morphism(x, y)
        x.morphismsTo[y].add(newMorphism)
        y.morphismsFrom[x].add(newMorphism)
        # newMorphism.category.morphisms.add(newMorphism)
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
        return newObject

    def _newMorphism(self, domain: Object, codomain: Object) -> Morphism:
        newMorphism = Morphism.construct(domain, codomain)
        self.morphisms.add(newMorphism)
        return newMorphism

    def someObject(self) -> Object:
        return self._newObject()

    def someMorphism(self, domain: Object, codomain: Object) -> Morphism:
        return self._newMorphism(domain, codomain)

class NamedObject(Object):
    def __init__(self, name: str, category: Category = None) -> None:
        """Omit category only when Object.__init__(category) has been called"""
        if category is not None:
            super().__init__(category)
        self.name = name
        self.identity.__class__ = NamedMorphism
        self.identity.name = f'{category.name}_morId{self.name}'
    
    def __repr__(self) -> str:
        return self.name

class NamedMorphism(Morphism):
    def __init__(self, domain: Object, codomain: Object, name: str) -> None:
        """`NamedMorphism()` should not be called. Use factory method `NamedMorphism.construct()`."""
        super().__init__(domain, codomain)
        self.name = name

    def __repr__(self) -> str:
        return self.name
    
    @classmethod
    def construct(cls, domain: Object, codomain: Object, name: str) -> Morphism:
        newMorphism = super().construct(domain, codomain, name=name)
        return newMorphism

class SerialNamedCategory(Category):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._objectCounter = itertools.count()
        self._morphismCounter = itertools.count()

    @property
    def _nextObjectId(self) -> int:
        return self._objectCounter.__next__()
    
    @property
    def _nextMorphismId(self) -> int:
        return self._morphismCounter.__next__()
    
    def _newObject(self) -> NamedObject:
        newObject = super()._newObject()
        newObject.__class__ = NamedObject
        name = f'{newObject.category.name}{self._nextObjectId}'
        NamedObject.__init__(newObject, name)
        return newObject
    
    def _newMorphism(self, domain: NamedObject, codomain: NamedObject) -> NamedMorphism:
        newMorphism = super()._newMorphism(domain, codomain)
        newMorphism.__class__ = NamedMorphism
        newMorphism.name = f'{newMorphism.category.name}_mor{self._nextMorphismId}'
        return newMorphism


A = Category('A')
print(A._nextObjectId, A._nextObjectId)
