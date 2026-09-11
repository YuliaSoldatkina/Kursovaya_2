"""Тесты для модуля file_handlers."""

import json
import os
import pytest
from src.models import Aeroplane
from src.file_handlers import JSONSaver


class TestJSONSaver:
    """Тесты класса JSONSaver."""

    @pytest.fixture
    def saver(self, tmp_path):
        """Создание JSONSaver с временным файлом."""
        filename = tmp_path / "test_aeroplanes.json"
        return JSONSaver(str(filename))

    @pytest.fixture
    def aeroplane(self):
        """Создание тестового самолёта."""
        return Aeroplane(
            callsign="TEST1",
            country="USA",
            velocity=200.0,
            altitude=5000.0,
            icao24="abc123"
        )

    def test_add_aeroplane(self, saver, aeroplane):
        """Добавление самолёта в файл."""
        saver.add_aeroplane(aeroplane)
        data = saver.get_aeroplanes()

        assert len(data) == 1
        assert data[0]["callsign"] == "TEST1"

    def test_get_aeroplanes_empty(self, saver):
        """Получение данных из пустого файла."""
        data = saver.get_aeroplanes()
        assert data == []

    def test_delete_aeroplane(self, saver, aeroplane):
        """Удаление самолёта из файла."""
        saver.add_aeroplane(aeroplane)
        saver.delete_aeroplane(aeroplane)
        data = saver.get_aeroplanes()

        assert len(data) == 0

    def test_no_duplicate_add(self, saver, aeroplane):
        """Проверка: дубликаты не добавляются."""
        saver.add_aeroplane(aeroplane)
        saver.add_aeroplane(aeroplane)
        data = saver.get_aeroplanes()

        assert len(data) == 1

    def test_file_created(self, saver):
        """Проверка: файл создаётся при инициализации."""
        assert os.path.exists(saver.filename)
