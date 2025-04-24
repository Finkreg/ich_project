# import mysql.connector
#
# # Функция в которой происходит запрос к базе данных
# def call_database(data):
#     dbconfig = {'host': 'ich-db.edu.itcareerhub.de',
#             'user': 'ich1',
#             'password': 'password',
#             'database': "sakila"}
#
#     connection = mysql.connector.connect(**dbconfig)
#
#     cursor = connection.cursor()
#     try:
#         cursor.execute(data)
#         result = cursor.fetchall()
#         print("=== ***** RESULT ***** ===")
#         for table in result:
#             print(table)
#     except mysql.connector.Error as err:
#         print("Query error: ", err)
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()