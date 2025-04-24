import search_log
import db_operation


def construct_query(criteria):
    select_clause = criteria.get('select_clause', "*")
    where_clauses = []
    genre = criteria.get('genre')
    year = criteria.get('year')
    year_operator = criteria.get('year_operator')
    limit = criteria.get('limit')
    order_by = criteria.get('order_by')
    film_name = criteria.get('film.title')

    query = (f"select distinct {select_clause} "
             f"from film join film_category on film_category.film_id = film.film_id "
             f"join category on category.category_id = film_category.category_id "
             f"join film_actor on film_actor.film_id = film.film_id "
             f"join actor on actor.actor_id = film_actor.actor_id ")

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
    print(where_clauses) # отладочный принт для контроля фильтра WHERE

    if order_by:
        query += f" ORDER BY {order_by}"

    if limit:
        query += f" LIMIT {limit}"
    print(query) #  отладочный принт для контроля запроса SQL выборки
    return query


def select_yes_no(prompt):
    while True:
        answer = input(f"{prompt}: (yes/no): ").strip().lower()
        if answer in ['yes', 'no']:
            return answer == 'yes'
        print("Invalid input. Please enter 'yes' or 'no'.")


def optional_input(prompt, validator = None):
    while True:
        value = input(f"{prompt}").strip()
        if not value:
            return None
        if validator is None or validator(value):
            return value
        print("Invalid input")


def search_films(criteria):
    query = construct_query(criteria)
    db_operation.call_database(query)


def get_search_criteria(username):
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

    search_log.log_user_search(username, search_list)
    return criteria


def show_all_genres():
    query = """select name from category"""
    db_operation.call_database(query)


def show_all_age_ratings():
    query = """select distinct rating from film """
    db_operation.call_database(query)


