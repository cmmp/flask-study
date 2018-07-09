import sqlite3

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

users = [
    (1, 'jose', 'asdf'),
    (2, 'rolf', '123'),
    (3, 'anne', '456')
]

insert_query = "INSERT INTO users VALUES (?, ?, ?)"

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

conn.commit()
conn.close()
