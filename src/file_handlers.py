"""Модуль для работы с файлами."""

from abc import ABC, abstractmethod
import json
import os

from src.models import Aeroplane


class BaseFileHandler(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Добавить информацию о самолёте в файл.

        :param aeroplane: Объект Aeroplane
        """
        pass

    @abstractmethod
    def get_aeroplanes(self) -> list[dict]:
        """
        Получить данные из файла.

        :return: Список словарей с данными о самолётах
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Удалить информацию о самолёте из файла.

        :param aeroplane: Объект Aeroplane
        """
        pass


class JSONSaver(BaseFileHandler):
    """Класс для сохранения данных в JSON-файл."""

    def __init__(self, filename: str = "data/aeroplanes.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Создать файл, если он не существует."""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавить самолёт в JSON-файл."""
        data = self.get_aeroplanes()
        aeroplane_dict = self._aeroplane_to_dict(aeroplane)

        # Проверка на дубликат
        for item in data:
            if item.get("icao24") == aeroplane.icao24:
                return  # Уже есть такой самолёт

        data.append(aeroplane_dict)
        self._save_to_file(data)

    def get_aeroplanes(self) -> list[dict]:
        """Получить все самолёты из файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удалить самолёт из файла по icao24."""
        data = self.get_aeroplanes()
        data = [
            item for item in data
            if item.get("icao24") != aeroplane.icao24
        ]
        self._save_to_file(data)

    def _save_to_file(self, data: list[dict]) -> None:
        """Сохранить данные в файл."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _aeroplane_to_dict(self, aeroplane: Aeroplane) -> dict:
        """Преобразовать объект Aeroplane в словарь."""
        return {
            "icao24": aeroplane.icao24,
            "callsign": aeroplane.callsign,
            "country": aeroplane.country,
            "velocity": aeroplane.velocity,
            "altitude": aeroplane.altitude,
            "origin_country": aeroplane.origin_country,
            "on_ground": aeroplane.on_ground,
            "time_position": aeroplane.time_position
        }
