"""Модуль для работы с API."""

from abc import ABC, abstractmethod
from typing import Any

import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def get_data(self, url: str, params: dict | None = None) -> Any:
        """
        Получить данные по URL с параметрами.

        :param url: URL для запроса
        :param params: Параметры запроса (словарь)
        :return: Данные в формате JSON
        """
        pass

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> dict:
        """
        Получить координаты страны (bounding box).

        :param country_name: Название страны
        :return: Словарь с координатами (south, north, west, east)
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country_name: str) -> list[dict]:
        """
        Получить информацию о самолётах над страной.

        :param country_name: Название страны
        :return: Список словарей с данными о самолётах
        """
        pass


class AeroplanesAPI(BaseAPI):
    """Класс для работы с API nominatim и opensky-network."""

    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.headers = {
            "User-Agent": "KursovayaProject/1.0 (yulia.soldatkina@example.com)"
        }

    def get_data(self, url: str, params: dict | None = None) -> Any:
        """Получить данные по URL с параметрами."""
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            print(f"Ошибка при запросе к {url}: {error}")
            return []

    def get_country_coordinates(self, country_name: str) -> dict:
        """Получить координаты страны (bounding box)."""
        params = {
            "q": country_name,
            "format": "json",
            "limit": 1
        }
        data = self.get_data(self.nominatim_url, params)

        if data and len(data) > 0:
            boundingbox = data[0].get("boundingbox", [])
            if len(boundingbox) == 4:
                return {
                    "south": float(boundingbox[0]),
                    "north": float(boundingbox[1]),
                    "west": float(boundingbox[2]),
                    "east": float(boundingbox[3])
                }
        return {}

    def get_aeroplanes(self, country_name: str) -> list[dict]:
        """Получить информацию о самолётах над страной."""
        coords = self.get_country_coordinates(country_name)

        if not coords:
            print(f"Не удалось получить координаты для страны: {country_name}")
            return []

        params = {
            "lamin": coords["south"],
            "lamax": coords["north"],
            "lomin": coords["west"],
            "lomax": coords["east"]
        }

        data = self.get_data(self.opensky_url, params)

        if data and "states" in data:
            return data["states"]
        return []
