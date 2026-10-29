"""Абстрактные базовые классы иерархии помещений."""

from abc import ABC, abstractmethod


class Premise(ABC):
    """Абстрактное помещение."""

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Название должно быть непустой строкой')
        self._name = value.strip()

    @abstractmethod
    def area(self):
        """Общая площадь, м2."""

    @abstractmethod
    def heating_power(self):
        """Тепловая мощность обогрева, Вт."""

    def __str__(self):
        return (f'{self.__class__.__name__} "{self.name}": '
                f'{self.area():.2f} м2, {self.heating_power():.0f} Вт')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r})'


class GroupPremise(Premise):
    """Помещение, состоящее из дочерних помещений."""

    def __init__(self, name):
        super().__init__(name)
        self._children = []

    def add(self, child):
        if not isinstance(child, Premise):
            raise TypeError('Дочерний элемент должен быть Premise')
        self._children.append(child)

    def area(self):
        return sum(c.area() for c in self._children)

    def heating_power(self):
        return sum(c.heating_power() for c in self._children)

    def __len__(self):
        return len(self._children)

    def __iter__(self):
        return iter(self._children)