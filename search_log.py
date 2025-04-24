import json
from collections import Counter


def log_user_search(username, words):
    try:
        with open("log.json", "r") as log:
            log_data = json.load(log)  # Загружаем существующие данные
    except FileNotFoundError:
        log_data = {}  # Если файл отсутствует, создаём пустой словарь

    # Добавляем или обновляем данные пользователя
    if username in log_data:
        log_data[username].extend(words)  # Добавляем новые слова к существующим
    else:
        log_data[username] = words  # Создаём новую запись для пользователя

    # Записываем обновлённые данные обратно в файл
    with open("log.json", "w") as log:
        json.dump(log_data, log, indent=4)

    print(f"Data for user '{username}' has been logged successfully.")



def show_users_searched_items(username):
    temp = {}
    try:
        # Open and load the log file
        with open("log.json", "r") as log:
            log_data = json.load(log)

        # Handle case where username does not exist
        if username not in log_data:
            print(f"No data found for user: {username}")
            return temp

        # Count occurrences of each search item for the user
        user_items = log_data[username]
        temp = dict(Counter(user_items))

        # Print the results
        print(f"Searched items for user '{username}':")
        for item, count in temp.items():
            print(f"{item}: {count} times")

    except FileNotFoundError:
        print("Log file not found.")
    except json.JSONDecodeError:
        print("Log file is corrupted or not in valid JSON format.")

    print(temp)


