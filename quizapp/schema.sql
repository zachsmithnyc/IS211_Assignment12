DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS quiz_results;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT
    );

CREATE TABLE quizzes (
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    subject TEXT NOT NULL, 
    length INTEGER NOT NULL, 
    date TEXT NOT NULL);

CREATE TABLE quiz_results (
    quiz_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL, 
    student_name TEXT NOT NULL, 
    score INTEGER NOT NULL, 
    FOREIGN KEY (quiz_id) REFERENCES quizzes (quiz_id),
    FOREIGN KEY (student_id) REFERENCES students (id)
    );

INSERT INTO students (name) VALUES ('John Smith');
INSERT INTO quizzes (subject, length, date) VALUES ('Python Basics', 5, 'February, 5th, 2015');
INSERT INTO quiz_results (quiz_id, student_id, student_name, score) VALUES (1, 1, 'John Smith', 85);