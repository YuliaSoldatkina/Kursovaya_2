"""Главный модуль программы."""

from src.api import AeroplanesAPI
from src.user_interface import user_interaction


def main():
    """Точка входа в программу."""
    api = AeroplanesAPI()
    user_interaction(api.get_aeroplanes)


if __name__ == "__main__":
    main()
