import sqlite3

database = sqlite3.connect("plandata")
cursor = database.cursor()
cursor.execute("SELECT * FROM user_info")
print(cursor.fetchone())
cursor.execute("SELECT * FROM user_data")
print(cursor.fetchone())
database.close()