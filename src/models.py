"""Модуль с классом Aeroplane."""

from dataclasses import dataclass


@dataclass
class Aeroplane:
    """Класс для представления самолёта."""

    callsign: str
    country: str
    velocity: float
    altitude: float
    icao24: str = ""
    origin_country: str = ""
    on_ground: bool = False
    time_position: int = 0

    def __post_init__(self):
        """Валидация данных после инициализации."""
        self._validate_data()

    def _validate_data(self):
        """Проверка корректности данных."""
        if not isinstance(self.callsign, str):
            raise TypeError("Callsign должен быть строкой")
        if not isinstance(self.country, str):
            raise TypeError("Country должен быть строкой")
        if not isinstance(self.velocity, (int, float)):
            raise TypeError("Velocity должен быть числом")
        if not isinstance(self.altitude, (int, float)):
            raise TypeError("Altitude должен быть числом")
        if self.velocity < 0:
            raise ValueError("Velocity не может быть отрицательным")
        # Altitude может быть отрицательным (ниже уровня моря)

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение по высоте (для сортировки)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude < other.altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        """Сравнение по высоте (для сортировки)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude > other.altitude

    def __eq__(self, other: object) -> bool:
        """Проверка равенства."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.icao24 == other.icao24

    @classmethod
    def cast_to_object_list(cls, data: list[list]) -> list["Aeroplane"]:
        """
        Преобразовать список списков в список объектов Aeroplane.

        :param data: Список списков с данными от API
        :return: Список объектов Aeroplane
        """
        aeroplanes = []
        for item in data:
            if len(item) >= 7:
                aeroplane = cls(
                    icao24=item[0],
                    callsign=item[1] if item[1] else "N/A",
                    origin_country=item[2],
                    time_position=item[3] if item[3] else 0,
                    on_ground=bool(item[4]),
                    velocity=float(item[9]) if item[9] else 0.0,
                    altitude=float(item[7]) if item[7] else 0.0,
                    country=item[2]
                )
                aeroplanes.append(aeroplane)
        return aeroplanes
