import json


def authenticate():
    print("-----=====***** Welcome to Movie Database *****=====-----")
    print("1. Register")
    print("2. Log in")

    try:
        with open("credentials.json", "r") as file:
            credentials = json.load(file)
    except FileNotFoundError:
        credentials = {}

    while True:
        choice = input("Please Register or log in: ")
        if choice == "1":
            name = input("Please enter your name: ")
            password = input("Please enter your password: ")
            if name in credentials:
                print("You have already registered. Please log in.")
                continue
            else:
                credentials[name] = password
                with open("credentials.json", "w") as file:
                    json.dump(credentials, file, indent=4)
                print(f"user {name} registered successfully")
        elif choice == "2":
            name = input("Please enter your name: ")
            password = input("Please enter your password: ")
            if credentials.get(name) == password:
                print("You have succefully logged in")
                return name
            else:
                print("You've entered wrong credentials. Please try again.'")
        elif choice == "q":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Try again.")
