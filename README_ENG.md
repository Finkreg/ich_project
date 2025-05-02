# Console Application for Working with the Sakila Database

## 1. Project Goal:

Using the knowledge gained during the Python Fundamentals course and summarizing it, write a program that implements a console interface to the Sakila database, which contains information about various movies.

**Main program tasks:**

* Provide the user with the ability to search for movies by keywords, as well as by year and genre.
* Display a list of the most frequently searched queries from users.
* To track queries, create a separate database on the educational SQL server and, for each user query, record the information about what they have searched for into the corresponding table.

## 2. Database Installation Instructions:

Separate database installation is not required. Connection to databases is established on the ICH educational server.
Environment Configuration:

1. Create a `.env` file in the project's root directory.
2. Copy the values from `.env.example`.
3. Fill in the file with real data.


## 3. Description of Available Application Commands:

1.  **Search films (custom criteria)**
    * Fully customizable search.
    * The user can select table fields to display in the query.
    * Optional selection of search criteria: by year, genre, keyword, or a combination of the criterias.
    * Ability to choose the number of displayed results and the field for sorting.

2.  **Search by genre and year**
    * Search for movies by a combination of genre and release year.
    * The query result includes: movie title, release year, and genre.
    * Up to 10 results are displayed.

3.  **Search by keyword**
    * Search for movies by a keyword in the titles.
    * The query result includes: movie title, release year, and genre (if the keyword is found in the title).
    * Up to 10 results are displayed.

4.  **Display all age ratings**
    * Output information about all possible movie age ratings and their descriptions.

5.  **Show user's most searched queries**
    * Output a list of the most frequently searched queries from users (including keywords, years, and genres).

## 4. Example of Use:

* Run the program (the `main.py` file). The main menu appears:

    ```
    ===== Main Menu =====
    1. Search films (custom criteria)
    2. Search by genre and year
    3. Search by keyword
    4. Display all age ratings
    5. Show user's most searched queries
    6. Exit
    ```

* Select search by genre and year, enter `2`, and press Enter. The program displays a list of available genres:

    ```
    Action
    Animation
    Children
    Classics
    Comedy
    Documentary
    Drama
    Family
    Foreign
    Games
    Horror
    Music
    New
    Sci-Fi
    Sports
    Travel
    Enter the movie genre to search:
    ```

* Enter `Comedy` and press Enter. The program asks for the year:

    ```
    Enter the year to search:
    ```

* Enter `1995` and press Enter. The program asks for a comparison operator:

    ```
    Enter a year operator (<, >, =):
    ```

* Enter `>` and press Enter. The program should output movies of the "Comedy" genre released after 1995:

    ```
    === ***** RESULT ***** ===
    AIRPLANE SIERRA - 1996 - Comedy
    ANTHEM LUKE - 2001 - Comedy
    BRINGING HYSTERICAL - 2018 - Comedy
    CAPER MOTIONS - 2003 - Comedy
    CAT CONEHEADS - 2014 - Comedy
    CLOSER BANG - 2021 - Comedy
    CONNECTION MICROCOSMOS - 2019 - Comedy
    CONTROL ANTHEM - 2017 - Comedy
    CRAZY HOME - 1996 - Comedy
    DADDY PITTSBURGH - 2006 - Comedy
    ```
The program then returns to the Main Menu and remains in standby mode, awaiting for the next command.