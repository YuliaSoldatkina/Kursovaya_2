"""Тесты для модуля user_interface."""

import pytest
from src.models import Aeroplane
from src.user_interface import (
    get_top_n_aeroplanes,
    filter_by_country,
    filter_by_altitude_range
)


class TestUserInterface:
    """Тесты функций user_interface."""

    @pytest.fixture
    def aeroplanes(self):
        """Создание тестовых самолётов."""
        return [
            Aeroplane("A1", "USA", 200, 5000),
            Aeroplane("A2", "Spain", 250, 8000),
            Aeroplane("A3", "USA", 300, 3000),
            Aeroplane("A4", "France", 150, 10000),
        ]

    def test_get_top_n_aeroplanes(self, aeroplanes):
        """Получение топ N самолётов по высоте."""
        top = get_top_n_aeroplanes(aeroplanes, 2)

        assert len(top) == 2
        assert top[0].altitude == 10000
        assert top[1].altitude == 8000

    def test_filter_by_country(self, aeroplanes):
        """Фильтрация по стране регистрации."""
        filtered = filter_by_country(aeroplanes, ["USA"])

        assert len(filtered) == 2
        assert all("USA" in a.country for a in filtered)

    def test_filter_by_altitude_range(self, aeroplanes):
        """Фильтрация по диапазону высот."""
        filtered = filter_by_altitude_range(aeroplanes, 4000, 9000)

        assert len(filtered) == 2
        assert all(4000 <= a.altitude <= 9000 for a in filtered)

    def test_get_top_n_zero(self, aeroplanes):
        """Получение топ 0 самолётов."""
        top = get_top_n_aeroplanes(aeroplanes, 0)
        assert len(top) == 0

    def test_filter_by_country_no_match(self, aeroplanes):
        """Фильтрация: нет совпадений."""
        filtered = filter_by_country(aeroplanes, ["Japan"])
        assert len(filtered) == 0
