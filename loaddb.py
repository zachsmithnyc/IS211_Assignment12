import sqlite3 as lite

DB_PATH = 'hw12.db'
person = (('John Smith'))
quiz = (('Python Basics', 5, '2015-02-5'))
quiz_result = (('John Smith', 85))

con = lite.connect(DB_PATH)

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS person")
    cur.execute("DROP TABLE IF EXISTS quiz")
    cur.execute("DROP TABLE IF EXISTS quiz_result")
    cur.execute("CREATE TABLE person (id INTEGER PRIMARY KEY ASC, name TEXT")
    cur.execute("CREATE TABLE quiz (quiz_id INTEGER PRIMARY KEY ASC, subject TEXT, length INTEGER, date INTEGER")
    cur.execute("CREATE TABLE quiz_result (quiz_id INTEGER, FOREIGN KEY (quiz_id) REFERENCES quiz (quiz_id), student_name TEXT, score INTEGER")

    cur.executemany("INSERT INTO person (name) VALUES (?), person")

    cur.executemany("INSERT INTO quiz (subject, length, date) VALUES (?, ?, ?), quiz")

    cur.executemany("INSERT INTO quiz_result (student_name, score) VALUES (?,?), quiz_result")
    