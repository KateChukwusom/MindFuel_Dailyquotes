import sqlite3

connection = sqlite3.connect("storage.db")
cur = connection.cursor()

#create users table
cur.execute("""
    CREATE TABLE IF NOT EXISTS  users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    status TEXT DEFAULT "Active",
    frequency TEXT DEFAULT 'daily'
) """)

print ("users table created successfully")
#create quotes table
cur.execute(""" 
    CREATE TABLE IF NOT EXISTS quotes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT NOT NULL,
    author TEXT NOT NULL
)""")
print ("quotes table creates successfully")

#insert users into the users table
cur.executemany("""INSERT OR IGNORE INTO users (name, email, status, frequency) VALUES (?, ?, ?, ?)
    """, [
    ("Chisom", "chisomokeke823@gmail.com", "active", "daily"),
    ("Kate", "okekekatesom@gmail.com", "inactive", "daily"),
    ("Raphael", "patraffiah@gmail.com", "active", "daily"),
    ("Victor", "mrmailerg2i@gmail.com", "active", "daily")
])

connection.commit()
connection.close()

print ("Database created successfully")
