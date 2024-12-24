import json
import os

file_path = "users.json"

# Функция для создания JSON файла, если его нет
def create_json_file(file_path, user_data):
    """
    Создаёт JSON файл с базовой структурой, если файла не существует.
    """
    if not os.path.exists(file_path):
        print("Файл не найден. Создаём новый JSON файл.")
        structured_data = {
            "users": [
                {
                    "user_id": user_id,
                    "name": name,
                    "date": "",  # Пустые значения для каждого поля
                    "arrival_time": "",
                    "tasks": "",
                    "result": "",
                    "problems": "",
                    "comments": ""
                }
                for user_id, name in user_data.items()
            ]
        }
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(structured_data, file, indent=4, ensure_ascii=False)
        print(f"Файл {file_path} создан.")
    else:
        print(f"Файл {file_path} уже существует.")

# Функция для чтения данных из JSON файла
def read_json_file(file_path):
    """
    Читает данные из JSON файла и возвращает их как словарь.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        print(f"Файл {file_path} не найден.")
        return None

# Функция для сохранения данных в JSON файл
def save_json_file(data, file_path="users.json"):
    """
    Сохранить данные в JSON файл.
    :param data: Данные, которые нужно сохранить.
    :param file_path: Путь к файлу.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Данные успешно сохранены.")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

# Обновление данных пользователя
def update_user_info(user_id, field, new_value, file_path="users.json"):
    """
    Обновить информацию о пользователе по указанному полю.
    
    :param user_id: ID пользователя.
    :param field: Поле для обновления (например, 'date', 'arrival_time', 'tasks' и т.д.).
    :param new_value: Новое значение, которое нужно установить.
    :param file_path: Путь к файлу.
    """
    try:
        # Чтение данных из JSON файла
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Поиск пользователя по user_id
        user_found = False
        for user in data["users"]:
            if user["user_id"] == user_id:
                # Обновление нужного поля
                if field == "date":
                    user["date"] = new_value  # Обновляем поле "date"
                elif field == "arrival_time":
                    user["arrival_time"] = new_value  # Обновляем поле "arrival_time"
                elif field == "tasks":
                    user["tasks"] = new_value  # Обновляем поле "tasks"
                elif field == "result":
                    user["result"] = new_value  # Обновляем поле "result"
                elif field == "problems":
                    user["problems"] = new_value  # Обновляем поле "problems"
                elif field == "comments":
                    user["comments"] = new_value  # Обновляем поле "comments"
                user_found = True
                break

        if not user_found:
            print(f"Пользователь с ID {user_id} не найден.")
            return

        # Сохранение обновленных данных в файл
        save_json_file(data, file_path)

    except Exception as e:
        print(f"Ошибка при обновлении данных: {e}")

# Summary для каждого пользователя 
def get_user_data(user_id, file_path):
    # Открываем файл и загружаем данные
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)  # Преобразуем строку JSON в словарь

    # Ищем пользователя по user_id
    users = json_data.get('users', [])
    user = next((user for user in users if user['user_id'] == str(user_id)), None)
    
    if user is None:
        return "Пользователь не найден."
    
    # Формируем итоговое сообщение
    summary = (
        f"📋 <b>Ваша планерка:</b>\n\n"
        f"📅 Дата планерки: <b>{user.get('date', '-')}</b>\n\n"
        f"⏰ Время прихода: <b>{user.get('arrival_time', '-')}</b>\n\n"
        f"🔴 Задачи: <b>{user.get('tasks', '-')}</b>\n\n"
        f"🟠 Итоги, Что выполнено/Что не выполнено✅❌: <b>{user.get('result', '-')}</b>\n\n"
        f"⚠️ Проблемы: <b>{user.get('problems', '-')}</b>\n\n"
        f"💬 Комментарии: <b>{user.get('comments', '-')}</b>"
    )
    
    return summary


# Функция очистки данных пользователя 
def clear_user_data(user_id, file_path):
    # Открываем JSON-файл
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Ищем пользователя с заданным user_id
    for user in json_data.get('users', []):
        if user.get('user_id') == user_id:
            # Очищаем поля
            user["date"] = ""
            user["arrival_time"] = ""
            user["tasks"] = ""
            user["result"] = ""
            user["problems"] = ""
            user["comments"] = ""
            break

    # Сохраняем изменения обратно в файл
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

