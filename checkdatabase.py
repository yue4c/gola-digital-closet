import sqlite3

connection = sqlite3.connect("gola.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM users")

users = cursor.fetchall()

for user in users:
    print(user)

connection.close()