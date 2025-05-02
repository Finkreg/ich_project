import mysql.connector
from datetime import datetime
from termcolor import colored
from dotenv import load_dotenv
import os

# --- Настройки подключения к основной базе данных ---
load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
# --- Настройки подключения к базе данных статистики ---
STATS_DB_CONFIG = {
    "host": os.getenv("STATS_DB_HOST"),
    "user": os.getenv("STATS_DB_USER"),
    "password": os.getenv("STATS_DB_PASSWORD"),
    "database": os.getenv("STATS_DB_NAME")
}


# Функция, которая возвращает подключение к базе данных или None, если произошла ошибка
def connect_db(config):
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None


# Функция, которая закрывает соединение
def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()


# Функция которая выполняет запрос, сохраняя внесенные изменения или же 
# откатываем изменения, если произошла ошибка. В конце закрываем объект курсора.
def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        return cursor
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()


# Функция которая возвращает данные извлеченные курсором
def fetch_results(cursor):
    try:
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching results: {err}")
        return None


# Функция которая записывает ключевые слова запроса в базу данных
def record_query(keywords):
    stats_conn = connect_db(STATS_DB_CONFIG)
    if stats_conn:
        cursor = stats_conn.cursor()
        try:
            # Создаем таблицу, если ее нет
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS popular_queries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    keyword VARCHAR(255) NOT NULL,
                    query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            stats_conn.commit()
            
            #Необходимо проверить тип ключевых слов. Если это строка, преобразую ее в список
            if isinstance(keywords, str):
                keywords = [keywords]

            for keyword in keywords:
                query = "INSERT INTO popular_queries (keyword) VALUES (%s)"
                cursor.execute(query, (keyword,))
            stats_conn.commit()
        except mysql.connector.Error as err:
            print(f"Error recording query: {err}")
            stats_conn.rollback()
        finally: 
            close_connection(stats_conn)


# Функция которая отображает запрашивает у базы данных наиболее популярные запросы и отображает их
def display_popular_queries():
    stats_conn = connect_db(STATS_DB_CONFIG)
    if stats_conn:
        cursor = stats_conn.cursor()
        try:
            cursor.execute("""
                SELECT keyword, COUNT(*) as popularity
                FROM popular_queries
                GROUP BY keyword
                ORDER BY popularity DESC
            """)
            popular_results = fetch_results(cursor)
            if popular_results:
                print(colored("\n=== Popular Search Queries ===", "green"))
                for keyword, popularity in popular_results:
                    print(f"- {keyword}: {popularity} times")
            else:
                print("No popular queries recorded yet.")
        except mysql.connector.Error as err:
            print(f"Error displaying popular queries: {err}")
        finally:
            close_connection(stats_conn)


# Функция которая вызывает базу данных, передает в нее сформированный запрос и выводит в консоль результаты.
def call_database(query):
    connection = connect_db(DB_CONFIG)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            result = fetch_results(cursor)
            print()
            print(colored("=== ***** RESULT ***** ===", "magenta"))
            if result:
                for row in result:
                    print(" - " .join(map(str, row)))
            else:
                print("No data found")
        except mysql.connector.Error as err:
            print(f"Query error: {err}")
        finally:
            close_connection(connection)
    return None