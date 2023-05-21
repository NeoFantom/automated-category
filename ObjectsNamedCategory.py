from baseCategory import *
from baseCategory import Morphism, Object

DEBUG_NAME = False

class NamedObject(Object):
    def __init__(self, name: str, category: Category = None) -> None:
        """Omit category only when Object.__init__(category) has been called"""
        if category is not None:
            super().__init__(category)
        self.name = name
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if DEBUG_NAME:
            name += '@' + object.__repr__(self)[-5:-1]
        self._name = name
        self.identity.__class__ = NamedMorphism
        self.identity.name = f'{self.category.name}_morId{self.name}'
    
    def __repr__(self) -> str:
        return self.name
    
class NamedMorphism(Morphism):
    def __init__(self, name: str, domain: Object = None, codomain: Object = None) -> None:
        """`NamedMorphism()` should not be called. Use factory method `NamedMorphism.construct()`."""
        if domain and codomain:
            super().__init__(domain, codomain)
        self.name = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if DEBUG_NAME:
            name += '@' + object.__repr__(self)[-5:-1]
        self._name = name

    def __repr__(self) -> str:
        return self.name
    
    def composeWith(self, another: 'NamedMorphism', name: str = '') -> 'NamedMorphism':
        if not name:
            name = f'{self}∘{another}'
        morphism = super().composeWith(another)
        morphism.__class__ = NamedMorphism
        morphism.name = name
        return morphism
    
    @classmethod
    def construct(cls, domain: Object, codomain: Object, name: str) -> Morphism:
        newMorphism = super().construct(domain, codomain, name=name)
        return newMorphism
    
class ObjectsNamedCategory(Category):
    """
    ObjectsNamedCategory ensures:
        - All objects are `NamedObject`
        - All morphisms are `NamedMorphism`
    """
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def someObject(self) -> Object:
        raise NotImplementedError()
    
    def someMorphism(self, domain: Object, codomain: Object) -> Morphism:
        raise NotImplementedError()
    
    def someObjectCalled(self, name: str) -> NamedObject:
        newObject = super().someObject()
        newObject.__class__ = NamedObject
        newObject.name = name
        return newObject
    
    def someMorphismCalled(self, name: str, domain: NamedObject, codomain: NamedObject) -> NamedMorphism:
        newMorphism = super().someMorphism(domain, codomain)
        newMorphism.__class__ = NamedMorphism
        newMorphism.name = name
        return newMorphism
    

if __name__ == '__main__':
    # DEBUG_NAME = True
    import sys
    sys.stdout = open('output', 'w', encoding='utf8')
    A = ObjectsNamedCategory('A')
    A0 = A.someObjectCalled('a')
    A1 = A.someObjectCalled('b')
    A2 = A.someObjectCalled('c')
    id0 = A0.identity
    id1 = A1.identity
    id2 = A2.identity
    f0 = A.someMorphismCalled('f', A0, A0)
    f1 = A.someMorphismCalled('g', A0, A1)
    f2 = A.someMorphismCalled('h', A1, A2)
    g = f1 @ f2
    mapinfo = lambda f: str((f, f.domain, f.codomain))
    newline = '\n\t\t'
    comma = ', '
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
        A0.morphismsTo
                {dict([
                    (Y, comma.join([mapinfo(m) for m in A0.morphismsTo[Y]]))
                    for Y in A0.morphismsTo])}
        A1.morphismsTo
                {dict([
                    (Y, comma.join([mapinfo(m) for m in A1.morphismsTo[Y]]))
                    for Y in A1.morphismsTo])}
        {A0.morphismsFrom[A0] == A0.morphismsTo[A0] = }
        {A0.morphismsTo[A1] == A1.morphismsFrom[A0] = }
        {mapinfo(g) = }
        """)