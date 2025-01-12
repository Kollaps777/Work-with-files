from typing import Dict, List, Union, Tuple
import os

def read_cook_book(file_path: str) -> Dict[str, List[Dict[str, Union[str, int]]]]:
    """
    Читает рецепты из файла и возвращает словарь с рецептами.

    :param file_path: Путь к файлу с рецептами.
    :return: Словарь, где ключ — название блюда, значение — список ингредиентов.
    :raises FileNotFoundError: Если файл не найден.
    :raises ValueError: Если файл имеет некорректный формат.
    """
    cook_book: Dict[str, List[Dict[str, Union[str, int]]]] = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                dish_name = file.readline().strip()
                if not dish_name:
                    break
                try:
                    ingredient_count = int(file.readline().strip())
                except ValueError:
                    raise ValueError(f"Некорректное количество ингредиентов для блюда '{dish_name}'")

                ingredients: List[Dict[str, Union[str, int]]] = []
                for _ in range(ingredient_count):
                    ingredient_line = file.readline().strip()
                    if not ingredient_line:
                        raise ValueError(f"Недостаточно ингредиентов для блюда '{dish_name}'")
                    parts = ingredient_line.split(' | ')
                    if len(parts) != 3:
                        raise ValueError(f"Некорректный формат ингредиента для блюда '{dish_name}': {ingredient_line}")
                    ingredient_name, quantity_str, measure = parts
                    try:
                        quantity = int(quantity_str)
                    except ValueError:
                        raise ValueError(f"Некорректное количество для ингредиента '{ingredient_name}' в блюде '{dish_name}'")
                    ingredients.append({
                        'ingredient_name': ingredient_name,
                        'quantity': quantity,
                        'measure': measure
                    })
                cook_book[dish_name] = ingredients
                file.readline()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не найден.")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла '{file_path}': {e}")

    return cook_book

def get_shop_list_by_dishes(dishes: List[str], person_count: int, cook_book: Dict[str, List[Dict[str, Union[str, int]]]]) -> Dict[str, Dict[str, Union[str, int]]]:
    """
    Возвращает список покупок для указанных блюд и количества персон.

    :param dishes: Список названий блюд.
    :param person_count: Количество персон.
    :param cook_book: Словарь с рецептами.
    :return: Словарь с ингредиентами и их количествами.
    """
    shop_list: Dict[str, Dict[str, Union[str, int]]] = {}
    for dish in dishes:
        if dish not in cook_book:
            print(f"Блюдо '{dish}' не найдено в книге рецептов.")
            continue
        for ingredient in cook_book[dish]:
            ingredient_name = ingredient['ingredient_name']
            quantity = ingredient['quantity'] * person_count
            measure = ingredient['measure']
            if ingredient_name in shop_list:
                shop_list[ingredient_name]['quantity'] += quantity
            else:
                shop_list[ingredient_name] = {'measure': measure, 'quantity': quantity}
    return shop_list

def merge_files(directory: str, output_file: str) -> None:
    """
    Объединяет файлы из указанной директории в один файл, сортируя их по количеству строк.

    :param directory: Путь к директории с файлами.
    :param output_file: Путь к выходному файлу.
    :raises FileNotFoundError: Если директория не найдена.
    """
    try:
        files_info: Dict[str, List[str]] = {}
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if not os.path.isfile(file_path):
                continue
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                files_info[filename] = lines

        sorted_files: List[Tuple[str, List[str]]] = sorted(files_info.items(), key=lambda x: len(x[1]))

        with open(output_file, 'w', encoding='utf-8') as out_file:
            for filename, lines in sorted_files:
                out_file.write(f"{filename}\n")
                out_file.write(f"{len(lines)}\n")
                out_file.writelines(lines)
    except FileNotFoundError:
        raise FileNotFoundError(f"Директория '{directory}' не найдена.")
    except Exception as e:
        raise ValueError(f"Ошибка при объединении файлов: {e}")

def main() -> None:
    # Задача №1
    try:
        cook_book = read_cook_book('recipes.txt')
        print("Cook Book:", cook_book)
    except Exception as e:
        print(f"Ошибка при чтении книги рецептов: {e}")

    # Задача №2
    try:
        shop_list = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2, cook_book)
        print("Shop List:", shop_list)
    except Exception as e:
        print(f"Ошибка при получении списка покупок: {e}")

    # Задача №3
    try:
        merge_files('files', 'files/merged_file.txt')
        print("Files merged successfully.")
    except Exception as e:
        print(f"Ошибка при объединении файлов: {e}")

if __name__ == "__main__":
    main()