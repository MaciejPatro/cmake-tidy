###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from abc import ABC, abstractmethod


class Element(ABC):
    def __init__(self):
        self._parent = None
        self._name = ''

    @property
    def parent(self) -> 'Element':
        return self._parent

    @parent.setter
    def parent(self, parent: 'Element'):
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @abstractmethod
    def add(self, component: 'Element') -> 'Element':
        pass

    @abstractmethod
    def accept(self, visitor):
        pass


class PrimitiveElement(Element):
    def __init__(self, name='', values=''):
        super().__init__()
        self._name = name
        self._values = values

    def __repr__(self) -> str:
        return f'{self.name}: {self.values}' if self.name != '' else ''

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = values

    def add(self, component: 'Element') -> 'Element':
        pass

    def accept(self, visitor):
        return visitor.visit(self.name, self.values)


class ComplexElement(Element):
    def __init__(self, name='') -> None:
        super().__init__()
        self._children = []
        self._name = name

    def __repr__(self) -> str:
        children_repr = [f'{self.name}.{self.__ident(str(child))}' for child in self._children if str(child) != '']
        return '\n'.join(children_repr)

    def __ident(self, representation: str) -> str:
        return representation.replace('\n', '\n{}'.format(' ' * (len(self.name) + 1)))

    def add(self, component: Element) -> 'Element':
        if component:
            self._children.append(component)
            component.parent = self
        return self

    def remove(self, component: Element) -> None:
        self._children.remove(component)
        component.parent = None

    def accept(self, visitor):
        values = [child.accept(visitor) for child in self._children]
        return visitor.visit(self.name, values)
