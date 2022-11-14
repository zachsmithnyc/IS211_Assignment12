DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS quiz;
DROP TABLE IF EXISTS quiz_result;

CREATE TABLE student (
    id INTEGER PRIMARY KEY ASC, 
    name TEXT
    );

CREATE TABLE quiz (
    quiz_id INTEGER PRIMARY KEY ASC, 
    subject TEXT, 
    length INTEGER, 
    date TEXT);

CREATE TABLE quiz_result (
    quiz_id INTEGER,
    student_id INTEGER, 
    student_name TEXT, 
    score INTEGER, 
    FOREIGN KEY (quiz_id) REFERENCES quiz (quiz_id),
    FOREIGN KEY (student_id) REFERENCES student (id)
    );