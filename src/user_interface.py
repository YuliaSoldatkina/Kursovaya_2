"""Модуль для взаимодействия с пользователем."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import Aeroplane


def print_aeroplanes(aeroplanes: list["Aeroplane"]) -> None:
    """Вывести список самолётов в консоль."""
    if not aeroplanes:
        print("Нет данных для отображения.")
        return

    print(f"\n{'='*60}")
    print(f"{'Самолёты':^60}")
    print(f"{'='*60}")

    for i, aeroplane in enumerate(aeroplanes, 1):
        line = (
            f"{i}. {aeroplane.callsign} | "
            f"Страна: {aeroplane.country} | "
            f"Высота: {aeroplane.altitude:.2f} м | "
            f"Скорость: {aeroplane.velocity:.2f} м/с"
        )
        print(line)

    print(f"{'='*60}\n")


def get_top_n_aeroplanes(
    aeroplanes: list["Aeroplane"],
    n: int
) -> list["Aeroplane"]:
    """
    Получить топ N самолётов по высоте.

    :param aeroplanes: Список самолётов
    :param n: Количество самолётов в топе
    :return: Отсортированный список из N самолётов
    """
    sorted_aeroplanes = sorted(
        aeroplanes,
        key=lambda x: x.altitude,
        reverse=True
    )
    return sorted_aeroplanes[:n]


def filter_by_country(
    aeroplanes: list["Aeroplane"],
    countries: list[str]
) -> list["Aeroplane"]:
    """
    Отфильтровать самолёты по стране регистрации.

    :param aeroplanes: Список самолётов
    :param countries: Список названий стран для фильтрации
    :return: Отфильтрованный список
    """
    return [
        aeroplane for aeroplane in aeroplanes
        if any(
            country.lower() in aeroplane.country.lower()
            for country in countries
        )
    ]


def filter_by_altitude_range(
    aeroplanes: list["Aeroplane"],
    min_alt: float,
    max_alt: float
) -> list["Aeroplane"]:
    """
    Отфильтровать самолёты по диапазону высот.

    :param aeroplanes: Список самолётов
    :param min_alt: Минимальная высота
    :param max_alt: Максимальная высота
    :return: Отфильтрованный список
    """
    return [
        aeroplane for aeroplane in aeroplanes
        if min_alt <= aeroplane.altitude <= max_alt
    ]


def user_interaction(get_aeroplanes_func) -> None:
    """
    Функция для взаимодействия с пользователем через консоль.

    :param get_aeroplanes_func: Функция для получения самолётов по стране
    """
    print("Добро пожаловать в систему мониторинга самолётов!")

    while True:
        print("\nВыберите действие:")
        print("1. Получить самолёты по стране")
        print("2. Получить топ N самолётов по высоте")
        print("3. Фильтровать по стране регистрации")
        print("4. Фильтровать по диапазону высот")
        print("5. Выход")

        choice = input("\nВведите номер действия: ").strip()

        if choice == "1":
            country = input("Введите название страны: ").strip()
            if not country:
                print("Название страны не может быть пустым!")
                continue

            aeroplanes_data = get_aeroplanes_func(country)
            aeroplanes = aeroplane_list_to_objects(aeroplanes_data)
            print_aeroplanes(aeroplanes)

        elif choice == "2":
            try:
                n_input = input("Введите количество самолётов (N): ").strip()
                n = int(n_input)
                if n <= 0:
                    print("N должно быть положительным числом!")
                    continue
            except ValueError:
                print("Введите корректное число!")
                continue

            country = input("Введите название страны: ").strip()
            aeroplanes_data = get_aeroplanes_func(country)
            aeroplanes = aeroplane_list_to_objects(aeroplanes_data)
            top = get_top_n_aeroplanes(aeroplanes, n)
            print_aeroplanes(top)

        elif choice == "3":
            countries_input = input(
                "Введите названия стран через пробел: "
            ).strip()
            countries = countries_input.split()
            if not countries:
                print("Список стран не может быть пустым!")
                continue

            country = input("Введите название страны для запроса: ").strip()
            aeroplanes_data = get_aeroplanes_func(country)
            aeroplanes = aeroplane_list_to_objects(aeroplanes_data)
            filtered = filter_by_country(aeroplanes, countries)
            print_aeroplanes(filtered)

        elif choice == "4":
            try:
                range_input = input(
                    "Введите диапазон высот (мин макс): "
                ).strip()
                parts = range_input.split()
                min_alt = float(parts[0])
                max_alt = float(parts[1])
                if min_alt < 0 or max_alt < 0:
                    print("Высоты не могут быть отрицательными!")
                    continue
                if min_alt > max_alt:
                    print("Мин высота должна быть меньше максимальной!")
                    continue
            except (ValueError, IndexError):
                print("Введите корректные числа!")
                continue

            country = input("Введите название страны для запроса: ").strip()
            aeroplanes_data = get_aeroplanes_func(country)
            aeroplanes = aeroplane_list_to_objects(aeroplanes_data)
            filtered = filter_by_altitude_range(aeroplanes, min_alt, max_alt)
            print_aeroplanes(filtered)

        elif choice == "5":
            print("До свидания!")
            break

        else:
            print("Некорректный выбор! Попробуйте снова.")


def aeroplane_list_to_objects(data: list[list]) -> list["Aeroplane"]:
    """Преобразовать список списков в список объектов Aeroplane."""
    from src.models import Aeroplane
    return Aeroplane.cast_to_object_list(data)


def user_interaction_with_file(saver) -> None:
    """
    Функция для взаимодействия с пользователем через консоль.
    Работает с данными из файла, а не из API.

    :param saver: Объект JSONSaver для работы с файлом
    """

    print("Добро пожаловать в систему мониторинга самолётов!")

    while True:
        print("\nВыберите действие:")
        print("1. Показать все самолёты")
        print("2. Получить топ N самолётов по высоте")
        print("3. Фильтровать по стране регистрации")
        print("4. Фильтровать по диапазону высот")
        print("5. Выход")

        choice = input("\nВведите номер действия: ").strip()

        if choice == "1":
            data = saver.get_aeroplanes()
            aeroplanes = _dict_list_to_aeroplanes(data)
            print_aeroplanes(aeroplanes)

        elif choice == "2":
            try:
                n_input = input("Введите количество самолётов (N): ").strip()
                n = int(n_input)
                if n <= 0:
                    print("N должно быть положительным числом!")
                    continue
            except ValueError:
                print("Введите корректное число!")
                continue

            data = saver.get_aeroplanes()
            aeroplanes = _dict_list_to_aeroplanes(data)
            top = get_top_n_aeroplanes(aeroplanes, n)
            print_aeroplanes(top)

        elif choice == "3":
            countries_input = input(
                "Введите названия стран через пробел: "
            ).strip()
            countries = countries_input.split()
            if not countries:
                print("Список стран не может быть пустым!")
                continue

            data = saver.get_aeroplanes()
            aeroplanes = _dict_list_to_aeroplanes(data)
            filtered = filter_by_country(aeroplanes, countries)
            print_aeroplanes(filtered)

        elif choice == "4":
            try:
                range_input = input(
                    "Введите диапазон высот (мин макс): "
                ).strip()
                parts = range_input.split()
                min_alt = float(parts[0])
                max_alt = float(parts[1])
                if min_alt < 0 or max_alt < 0:
                    print("Высоты не могут быть отрицательными!")
                    continue
                if min_alt > max_alt:
                    print("Мин высота должна быть меньше максимальной!")
                    continue
            except (ValueError, IndexError):
                print("Введите корректные числа!")
                continue

            data = saver.get_aeroplanes()
            aeroplanes = _dict_list_to_aeroplanes(data)
            filtered = filter_by_altitude_range(aeroplanes, min_alt, max_alt)
            print_aeroplanes(filtered)

        elif choice == "5":
            print("До свидания!")
            break

        else:
            print("Некорректный выбор! Попробуйте снова.")


def _dict_list_to_aeroplanes(data: list[dict]) -> list["Aeroplane"]:
    """Преобразовать список словарей в список объектов Aeroplane."""
    from src.models import Aeroplane
    aeroplanes = []
    for item in data:
        aeroplane = Aeroplane(
            icao24=item.get("icao24", ""),
            callsign=item.get("callsign", "N/A"),
            origin_country=item.get("origin_country", ""),
            time_position=item.get("time_position", 0),
            on_ground=item.get("on_ground", False),
            velocity=item.get("velocity", 0.0),
            altitude=item.get("altitude", 0.0),
            country=item.get("country", "")
        )
        aeroplanes.append(aeroplane)
    return aeroplanes
