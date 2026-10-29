"""Модуль: Многоэтажный дом."""

from .base import GroupPremise
from .apartment import Apartment


class House(GroupPremise):
    """Многоэтажный дом: состоит из квартир."""

    def __init__(self, name, floors=1):
        super().__init__(name)
        self.floors = floors

    @property
    def floors(self):
        return self._floors

    @floors.setter
    def floors(self, value):
        value = int(value)
        if value < 1:
            raise ValueError('Этажей должно быть >= 1')
        self._floors = value

    def add_apartment(self, apartment):
        if not isinstance(apartment, Apartment):
            raise TypeError('В дом можно добавлять только Apartment')
        self.add(apartment)

    def rooms_count(self):
        return sum(len(a) for a in self)

    def __str__(self):
        return (f'Дом "{self.name}": квартир: {len(self)}, комнат: {self.rooms_count()}, '
                f'{self.area():.2f} м2, {self.heating_power():.0f} Вт')

    def __repr__(self):
        return f'House({self.name!r}, apartments={len(self)}, floors={self.floors})'