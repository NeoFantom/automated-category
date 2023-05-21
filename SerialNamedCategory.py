import itertools
from baseCategory import Morphism, Object
from objectsNamedCategory import *
from objectsNamedCategory import NamedMorphism


class SerialNamedMorphism(NamedMorphism):
    def __init__(self, name: str, domain: Object = None, codomain: Object = None) -> None:
        if domain.category.__class__ != SerialNamedCategory:
            raise Exception('`SerialNamedMorphism` must live in a `SerialNamedCategory`')
        super().__init__(name, domain, codomain)

    def composeWith(self, another: NamedMorphism) -> NamedMorphism:
        print('SerialNamedMorphism.composeWith', self, another, 'is called')
        cat: SerialNamedCategory = self.category
        name = f'{cat.name}_mor{cat._nextMorphismId}'
        morphism = super().composeWith(another, name)
        morphism.__class__ = SerialNamedMorphism
        return morphism


class SerialNamedCategory(ObjectsNamedCategory):
    """
    SerialNamedCategory ensures:
        - All objects are `NamedObject`
        - All morphisms are `SerialNamedMorphism`
    """
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
    
    def someObject(self) -> Object:
        return super().someObjectCalled(name = f'{self.name}{self._nextObjectId}')
    
    def someMorphism(self, domain: Object, codomain: Object) -> Morphism:
        newMorphism = super().someMorphismCalled(name = f'{self.name}_mor{self._nextMorphismId}',
                                          domain=domain, codomain=codomain)
        newMorphism.__class__ = SerialNamedMorphism
        return newMorphism


if __name__ == '__main__':

    ############################### test basic operations & compose ###############################
    # DEBUG_NAME = True
    import sys
    sys.stdout = open('output', 'w', encoding='utf8')
    A = SerialNamedCategory('A')
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
    h = id0 @ f0
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