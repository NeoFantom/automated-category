import itertools
from ObjectsNamedCategory import *


class SerialNamedCategory(BaseCategory):
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