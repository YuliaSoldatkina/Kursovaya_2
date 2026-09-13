"""Главный модуль программы."""

from src.api import AeroplanesAPI
from src.file_handlers import JSONSaver
from src.models import Aeroplane
from src.user_interface import user_interaction_with_file


def main():
    """Точка входа в программу."""
    api = AeroplanesAPI()
    saver = JSONSaver()

    # Запрос страны у пользователя
    # Запрос страны у пользователя
    country = input(
        "Введите название страны для получения данных о самолётах: "
    ).strip()
    if not country:
        print("Название страны не может быть пустым!")
        return

    # Получение данных из API
    print(f"Получаем данные о самолётах над страной: {country}...")
    aeroplanes_data = api.get_aeroplanes(country)

    if not aeroplanes_data:
        print("Не удалось получить данные о самолётах или их нет.")
        return

    # Преобразование в объекты и сохранение в файл
    aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)

    # Очистка файла перед записью
    saver._save_to_file([])

    # Сохранение каждого самолёта
    for aeroplane in aeroplanes:
        saver.add_aeroplane(aeroplane)

    print(f"Сохранено {len(aeroplanes)} самолётов в файл.")

    # Запуск взаимодействия с пользователем
    user_interaction_with_file(saver)


if __name__ == "__main__":
    main()
