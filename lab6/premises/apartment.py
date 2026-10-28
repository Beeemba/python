"""Модуль 2: Квартира (состоит из комнат)."""

from .room import Room


class Apartment:
    """Квартира: список комнат."""

    def __init__(self, name):
        self.name = name
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def total_area(self):
        """Общая площадь квартиры, м2."""
        return sum(r.area() for r in self.rooms)

    def total_heating_power(self):
        """Общая тепловая мощность квартиры, Вт."""
        return sum(r.heating_power() for r in self.rooms)