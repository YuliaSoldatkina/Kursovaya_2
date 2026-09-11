"""Тесты для модуля api."""

import pytest
from src.api import AeroplanesAPI


class TestAeroplanesAPI:
    """Тесты класса AeroplanesAPI."""

    @pytest.fixture
    def api(self):
        """Создание экземпляра API."""
        return AeroplanesAPI()

    def test_api_initialization(self, api):
        """Проверка инициализации API."""
        assert api.nominatim_url is not None
        assert api.opensky_url is not None
        assert api.headers is not None

    def test_get_country_coordinates_empty(self, api):
        """Получение координат для несуществующей страны."""
        coords = api.get_country_coordinates("NonExistentCountry12345")
        assert isinstance(coords, dict)

    def test_get_aeroplanes_empty(self, api):
        """Получение самолётов для несуществующей страны."""
        aeroplanes = api.get_aeroplanes("NonExistentCountry12345")
        assert isinstance(aeroplanes, list)
