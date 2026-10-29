"""Модуль: Комната."""

from .base import Premise

HEAT_POWER_PER_M3 = 40


class Room(Premise):
    """Комната с managed-атрибутами width, length, height."""

    def __init__(self, name, width, length, height):
        super().__init__(name)
        self.width = width
        self.length = length
        self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError('Ширина должна быть > 0')
        self._width = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError('Длина должна быть > 0')
        self._length = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError('Высота должна быть > 0')
        self._height = value

    def area(self):
        return self.width * self.length

    def volume(self):
        return self.area() * self.height

    def heating_power(self):
        return self.volume() * HEAT_POWER_PER_M3

    def __str__(self):
        return (f'Комната "{self.name}": {self.width}x{self.length}x{self.height} м, '
                f'{self.area():.2f} м2, {self.heating_power():.0f} Вт')

    def __repr__(self):
        return f'Room({self.name!r}, {self.width}, {self.length}, {self.height})'