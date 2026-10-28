"""Модуль 3: Многоэтажный дом (состоит из квартир)."""

from .apartment import Apartment


class House:
    """Многоэтажный дом: список квартир."""

    def __init__(self, name):
        self.name = name
        self.apartments = []

    def add_apartment(self, apartment):
        self.apartments.append(apartment)

    def total_area(self):
        """Общая площадь дома, м2."""
        return sum(a.total_area() for a in self.apartments)

    def total_heating_power(self):
        """Общая тепловая мощность дома, Вт."""
        return sum(a.total_heating_power() for a in self.apartments)

    def rooms_count(self):
        """Всего комнат в доме."""
        return sum(len(a.rooms) for a in self.apartments)