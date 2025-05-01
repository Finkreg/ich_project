# Импорт необходимых модулей
import process_queries # Импорт модуля обработки запросов
import db_operation # Импорт модуля работы с базой данных
from termcolor import colored# Импорт модуля для добавления цвета в консольный вывод


# Функция, которая реализует главное меню приложения.
def main_menu():
    print(colored(f"::::: Welcome to the Movie Database! :::::", "red"))
    while True:
        print(colored("\n===== Main Menu =====", "green"))
        print("1. Search films (custom criteria)")
        print("2. Search by genre and year")
        print("3. Search by keyword")
        print("4. Display all age ratings")
        print("5. Show user's most searched queries: ")
        print("6. Exit")
        print()

        choice = input("Your choice: ")
        if choice == "1":
            search_criteria = process_queries.get_search_criteria()
            process_queries.search_films(search_criteria)
        elif choice == "2":
            process_queries.show_all_genres()
            process_queries.search_by_genre_and_year()
        elif choice == "3":
            process_queries.search_by_keyword()
        elif choice == "4":
            process_queries.show_all_age_ratings()
        elif choice == "5":
            db_operation.display_popular_queries()
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")

# Точка запуска приложения
if __name__ =="__main__":
    main_menu()