from main_utils import execute_query

"""This is so you can see the pre-entered data in my database."""

query1 = "SELECT * FROM user_info"
print(execute_query(query1, True))

query2 = "SELECT * FROM user_data"
print(execute_query(query2, True))