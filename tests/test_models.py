"""Тесты для модуля models."""

import pytest
from src.models import Aeroplane


class TestAeroplane:
    """Тесты класса Aeroplane."""

    def test_create_aeroplane(self):
        """Создание самолёта с корректными данными."""
        aeroplane = Aeroplane(
            callsign="UAL1621",
            country="United States",
            velocity=268.79,
            altitude=10203.18
        )
        assert aeroplane.callsign == "UAL1621"
        assert aeroplane.country == "United States"
        assert aeroplane.velocity == 268.79
        assert aeroplane.altitude == 10203.18

    def test_aeroplane_comparison_by_altitude(self):
        """Сравнение самолётов по высоте."""
        plane1 = Aeroplane("A1", "USA", 200, 5000)
        plane2 = Aeroplane("A2", "USA", 250, 8000)

        assert plane1 < plane2
        assert plane2 > plane1

    def test_aeroplane_validation_negative_velocity(self):
        """Проверка валидации: отрицательная скорость."""
        with pytest.raises(ValueError):
            Aeroplane("A1", "USA", -100, 5000)

    def test_aeroplane_validation_negative_altitude(self):
        """Проверка валидации: отрицательная высота."""
        with pytest.raises(ValueError):
            Aeroplane("A1", "USA", 100, -5000)

    def test_aeroplane_validation_wrong_type(self):
        """Проверка валидации: неверный тип данных."""
        with pytest.raises(TypeError):
            Aeroplane(123, "USA", 100, 5000)

    def test_cast_to_object_list(self):
        """Преобразование списка списков в объекты."""
        data = [
            ["icao1", "CALL1", "USA", 12345, False, 0, 0, 5000, 0, 200],
            ["icao2", "CALL2", "Spain", 12346, False, 0, 0, 8000, 0, 250]
        ]
        aeroplanes = Aeroplane.cast_to_object_list(data)

        assert len(aeroplanes) == 2
        assert aeroplanes[0].callsign == "CALL1"
        assert aeroplanes[1].altitude == 8000
