import mysql.connector
from datetime import datetime

# --- Настройки подключения к основной базе данных ---
DB_CONFIG = {'host': 'ich-db.edu.itcareerhub.de',
             'user': 'ich1',
             'password': 'password',
             'database': "sakila"}

# --- Настройки подключения к базе данных статистики ---
STATS_DB_CONFIG = {'host': 'localhost',
                   'user': 'your_stats_user',
                   'password': 'your_stats_password',
                   'database': 'popular_queries'}


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


# Функция которая выполняет запрос
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


# Функция которая возвращает данные курсора
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
                print("\n=== Popular Search Queries ===")
                for keyword, popularity in popular_results:
                    print(f"- {keyword}: {popularity} times")
            else:
                print("No popular queries recorded yet.")
        except mysql.connector.Error as err:
            print(f"Error displaying popular queries: {err}")
        finally:
            close_connection(stats_conn)


# Функция которая вызывает базу данных
def call_database(data):
    connection = connect_db(DB_CONFIG)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(data)
            result = fetch_results(cursor)
            print("=== ***** RESULT ***** ===")
            for row in result:
                print(row)
            return result
        except mysql.connector.Error as err:
            print(f"Query error: {err}")
        finally:
            close_connection(connection)
    return None