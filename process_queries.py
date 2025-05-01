import db_operation # Импорт модуля, который взаимодействует с базой данных


# Функция которая собирает строку SQL запроса к базе данных на основе собраных и переданых
# в качестве аргумента критериев. 
def construct_query(criteria):
    select_clause = criteria.get('select_clause', "*")
    where_clauses = []
    genre = criteria.get('genre')
    year = criteria.get('year')
    year_operator = criteria.get('year_operator')
    limit = criteria.get('limit')
    order_by = criteria.get('order_by')
    film_name = criteria.get('film.title')

    query = (f"select {select_clause} "
             f"from film join film_category on film_category.film_id = film.film_id "
             f"join category on category.category_id = film_category.category_id ")

    if film_name:
        query = query + f"WHERE film.title LIKE '%{film_name}%' "

    if genre:
        where_clauses.append(f"category.name = '{genre}'")

    if year and year.isdigit() and year_operator in ["<", ">", "="]:
        where_clauses.append(f"film.release_year {year_operator} {year}")

    if where_clauses:
        if film_name:
            query = query + f" AND {' AND '.join(where_clauses)} "
        else:
            query += f" WHERE {' AND '.join(where_clauses)}"
    # print(where_clauses) # дебаг принт для контроля фильтра WHERE

    if order_by:
        query += f" ORDER BY {order_by}"

    if limit:
        query += f" LIMIT {limit}"
    # print(query) #  дебаг принт для контроля запроса SQL выборки
    return query


# Функция которая обрабатывает ввод yes/no. Создана для сокращения кода
def select_yes_no(prompt):
    while True:
        answer = input(f"{prompt}: (yes/no): ").strip().lower()
        if answer in ['yes', 'no']:
            return answer == 'yes'
        print("Invalid input. Please enter 'yes' or 'no'.")


# Функция которая обрабатывает опциональный ввод. Создана для сокращения кода
def optional_input(prompt, validator = None):
    while True:
        value = input(f"{prompt}").strip()
        if not value:
            return None
        if validator is None or validator(value):
            return value
        print("Invalid input")


# Функция которая получает критериии, вызывает функцию формирующую SQL запрос, а 
# затем запускает другую функцию, которая передает запрос в базу данных
def search_films(criteria):
    query = construct_query(criteria)
    db_operation.call_database(query)


# Функция которая формирует словарь критериев для последующей передачи в функцию, 
# которая на основе этих данных формирует SQL запрос.
def get_search_criteria():
    criteria = {}
    fields_to_select_sql = []

    if select_yes_no("Show title"):
        fields_to_select_sql.append("film.title")

    if select_yes_no("Show release year"):
        fields_to_select_sql.append("film.release_year")

    if select_yes_no("Show description"):
        fields_to_select_sql.append("film.description")

    if select_yes_no("Show age rating"):
        fields_to_select_sql.append("film.rating")


    if fields_to_select_sql:
        criteria["select_clause"] = ", ".join(fields_to_select_sql)
    else:
        criteria["select_clause"] = "*"

    search_list = []

    film_name = optional_input("(OPTIONAL) Enter the full or part name of the film: ")
    if film_name:
        criteria["film.title"] = film_name
        search_list.append(film_name)

    genre = optional_input("(OPTIONAL) Enter genre to search: ")
    if genre:
        criteria["genre"] = genre
        search_list.append(genre)

    year = optional_input("(OPTIONAL) Enter year: ", str.isdigit)
    if year:
        criteria["year"] = year
        search_list.append(year)
        operator = optional_input("Enter a year operator(<, >, = :)", lambda x: x in["<", ">", "="])
        if operator:
            criteria["year_operator"] = operator

    limit = optional_input("(OPTIONAL) Enter the number of results to limit: ", str.isdigit)
    if limit:
        criteria["limit"] = limit

    order_by_options = ['title', 'release_year', 'description', 'genre']
    order_by = optional_input("(OPTIONAL) Enter field to order by: "
                         "possible values: 'title', 'release_year', 'description', 'genre': ",
                         lambda x: x in order_by_options)
    if order_by:
        criteria["order_by"] = order_by

    db_operation.record_query(search_list)
    return criteria


# Функция которая выводит на экран все жанры из базы данных
def show_all_genres():
    query = """select name from category"""
    db_operation.call_database(query)


# Функция которая выводит на экран возрастные рейтинги и предоставляет
# их расшифровку
def show_all_age_ratings():
    query = """SELECT distinct rating,
            CASE
                WHEN rating = 'PG' THEN "Parental Guidance Suggested"
                WHEN rating = 'G' THEN "General Audiences"
                WHEN rating = 'NC-17' THEN "Adults Only"
                WHEN rating = 'PG-13' THEN "Parents Strongly Cautioned"
                WHEN rating  = 'R' THEN "Restricted"
            END as adviced_rating
            FROM film;
            """
    db_operation.call_database(query)


# Функция которая реализует поиск по жанру и году
def search_by_genre_and_year():

    user_genre, user_year, year_operator = None, None, None
    search_queries = []

    while not user_genre:    
        user_genre = input("Enter the film genre to search: ").strip()
        search_queries.append(user_genre)
        if not user_genre:
            print("Genre cannot be empty")
    while not user_year or not user_year.isdigit():
        user_year = input("Enter the year to search: ").strip()
        search_queries.append(user_year)
        if not user_year:
            print("Year must be a number")
    while year_operator not in['<', '>', '=']:
        year_operator = input("Enter a year operator (<, >, =): ").strip()
        if year_operator not in ['<', '>', '=']:
            print("Invalid operator! Use <, >, or =.")

    query = f"""
    SELECT film.title, film.release_year, category.name AS genre
    FROM film
    JOIN film_category ON film_category.film_id = film.film_id
    JOIN category ON category.category_id = film_category.category_id
    WHERE category.name = '{user_genre}' AND film.release_year {year_operator} {user_year} 
    LIMIT 10"""
    db_operation.record_query(search_queries)
    db_operation.call_database(query)


# Функция которая реализует поиск по ключевому слову
def search_by_keyword():
    while True:
        keyword = input("Enter a keyword to search for: ")
        if keyword:
            query = f"""SELECT film.title, film.release_year, category.name AS genre
    FROM film
    JOIN film_category ON film_category.film_id = film.film_id
    JOIN category ON category.category_id = film_category.category_id
    WHERE film.title LIKE '%{keyword}%' 
    LIMIT 10"""
            break
        else: continue
    db_operation.record_query(keyword)
    db_operation.call_database(query)
