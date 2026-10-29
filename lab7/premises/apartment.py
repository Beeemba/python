"""Модуль: Квартира."""

from .base import GroupPremise
from .room import Room


class Apartment(GroupPremise):
    """Квартира: состоит из комнат."""

    def __init__(self, name):
        super().__init__(name)

    def add_room(self, room):
        if not isinstance(room, Room):
            raise TypeError('В квартиру можно добавлять только Room')
        self.add(room)

    def __str__(self):
        return (f'Квартира "{self.name}": комнат: {len(self)}, '
                f'{self.area():.2f} м2, {self.heating_power():.0f} Вт')

    def __repr__(self):
        return f'Apartment({self.name!r}, rooms={len(self)})'