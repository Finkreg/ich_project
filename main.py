import process_queries
import search_log
import user_auth
import db_operation



def main_menu():
    name = user_auth.authenticate()
    print(f"Welcome, {name}")
    while True:
        print("\n=== Main Menu ===")
        print("1. Search films (custom criteria)")
        print("2. Display all genres")
        print("3. Display all age ratings")
        print("4. Show user's most searched queries: ")
        print("5. Exit")
        print()

        choice = input("Your choice: ")
        if choice == "1":
            search_criteria = process_queries.get_search_criteria(name)
            process_queries.search_films(search_criteria)
        elif choice == "2":
            process_queries.show_all_genres()
        elif choice == "3":
            process_queries.show_all_age_ratings()
        elif choice == "4":
            #search_log.show_users_searched_items(name)
            db_operation.display_popular_queries()
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")


main_menu()