"""Модуль 1: Комната."""

HEAT_POWER_PER_M3 = 40  


class Room:
    """Комната: ширина, длина, высота потолка."""

    def __init__(self, name, width, length, height):
        self.name = name
        self.width = width
        self.length = length
        self.height = height

    def area(self):
        """Площадь комнаты, м2."""
        return self.width * self.length

    def volume(self):
        """Объем комнаты, м3."""
        return self.area() * self.height

    def heating_power(self):
        """Тепловая мощность для обогрева, Вт."""
        return self.volume() * HEAT_POWER_PER_M3