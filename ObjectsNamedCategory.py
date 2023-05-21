from BaseCategory import *


class NamedObject(BaseObject):
    def __init__(self, name: str, category: BaseCategory = None) -> None:
        """Omit category only when Object.__init__(category) has been called"""
        if category is not None:
            super().__init__(category)
        self.name = name
    
    def __repr__(self) -> str:
        return self.name
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.identity.__class__ = NamedMorphism
        self.identity.name = f'{self.category.name}_morId{self.name}'
    
class NamedMorphism(BaseMorphism):
    def __init__(self, name: str, domain: BaseObject = None, codomain: BaseObject = None) -> None:
        """`NamedMorphism()` should not be called. Use factory method `NamedMorphism.construct()`."""
        if domain and codomain:
            super().__init__(domain, codomain)
        self.name = name

    def __repr__(self) -> str:
        return self.name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        print('NamedMorphism.name.setter() is called')
        self._name = name
    
    @classmethod
    def construct(cls, domain: BaseObject, codomain: BaseObject, name: str) -> BaseMorphism:
        newMorphism = super().construct(domain, codomain, name=name)
        return newMorphism
    
class ObjectsNamedCategory(BaseCategory):
    pass