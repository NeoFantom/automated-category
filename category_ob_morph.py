from typing import Any
import itertools

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
        self.identity = Morphism(domain=self, codomain=self)
        category.morphisms.add(self.identity)
        self.morphismsTo = {self: {self.identity}}
        self.morphismsFrom = {self: {self.identity}}

class Morphism:
    def __init__(self, domain: Object, codomain: Object) -> None:
        if domain.category != codomain.category:
            raise MorphismCategoryError('domain and codomain must be objects within the same category')
        self.category = domain.category
        self.domain = domain
        self.codomain = codomain
    
    @classmethod
    def construct(cls, domain: Object, codomain: Object) -> Morphism:
        newMorphism = Morphism(domain, codomain)
        if domain not in codomain.morphismsFrom:
            codomain.morphismsFrom[domain] = 
        
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
        newMorphism = Morphism(domain, codomain)
        self.morphisms.add(newMorphism)

    def anyObject(self) -> Object:
        return self._newObject()

    def anyMorphism(self, domain: Object, codomain: Object) -> Morphism:
        return self._newMorphism(domain, codomain)

class NamedObject(Object):
    def __init__(self, category: Category, name: str) -> None:
        super().__init__(category)
        self.name = name
        self.identity.__class__ = NamedMorphism
        self.identity.name = f'{category.name}_morId{self.name}'
    
    def __repr__(self) -> str:
        return self.name

class NamedMorphism(Morphism):
    def __init__(self, domain: Object, codomain: Object, name: str) -> None:
        super().__init__(domain, codomain)
        self.name = name

    def __repr__(self) -> str:
        return self.name

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
        newObject.name = f'{newObject.category.name}{self._nextObjectId}'
        return newObject
    
    def _newMorphism(self, domain: NamedObject, codomain: NamedObject) -> NamedMorphism:
        newMorphism = super()._newMorphism(domain, codomain)
        newMorphism.__class__ = NamedMorphism
        newMorphism.name = f'{newMorphism.category.name}_mor{self._nextMorphismId}'
        return newMorphism


A = Category('A')
print(A._nextObjectId, A._nextObjectId)
