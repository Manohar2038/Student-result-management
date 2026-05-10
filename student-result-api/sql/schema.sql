-- ─────────────────────────────────────────────────────────
-- Student Result Management System — Full MySQL Schema
-- Run: mysql -u root -p < sql/schema.sql
-- ─────────────────────────────────────────────────────────

CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

-- ── 1. students ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
    id          INT           AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    roll_number VARCHAR(20)   NOT NULL UNIQUE,
    department  VARCHAR(50)   NOT NULL,
    semester    TINYINT       NOT NULL CHECK (semester BETWEEN 1 AND 8),
    created_at  TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ── 2. subjects ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS subjects (
    id      INT          AUTO_INCREMENT PRIMARY KEY,
    code    VARCHAR(10)  NOT NULL UNIQUE,
    name    VARCHAR(80)  NOT NULL,
    credits TINYINT
);

-- ── 3. results ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS results (
    id         INT           AUTO_INCREMENT PRIMARY KEY,
    student_id INT           NOT NULL,
    gpa        DECIMAL(3,1)  NOT NULL,
    grade      CHAR(1)       NOT NULL,
    semester   TINYINT,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- ── 4. enrollments ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS enrollments (
    id          INT   AUTO_INCREMENT PRIMARY KEY,
    student_id  INT,
    subject_id  INT,
    enrolled_on DATE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

-- ── 5. marks_detail ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS marks_detail (
    id         INT           AUTO_INCREMENT PRIMARY KEY,
    student_id INT           NOT NULL,
    subject_id INT           NOT NULL,
    marks      DECIMAL(5,2)  NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

-- ── Stored Procedure ─────────────────────────────────────
DROP PROCEDURE IF EXISTS recalculate_grades;

DELIMITER $$
CREATE PROCEDURE recalculate_grades()
BEGIN
    UPDATE results r
    JOIN (
        SELECT student_id, AVG(marks) AS avg_marks
        FROM marks_detail
        GROUP BY student_id
    ) m ON r.student_id = m.student_id
    SET r.grade = CASE
        WHEN m.avg_marks >= 90 THEN 'A'
        WHEN m.avg_marks >= 75 THEN 'B'
        WHEN m.avg_marks >= 60 THEN 'C'
        ELSE                        'F'
    END;
END$$
DELIMITER ;

-- ── Sample Data ──────────────────────────────────────────
INSERT INTO students (name, roll_number, department, semester) VALUES
    ('Arjun Sharma', 'CS2301', 'CSE',   5),
    ('Priya Nair',   'EC2302', 'ECE',   3),
    ('Rahul Mehta',  'ME2303', 'MECH',  7),
    ('Sneha Iyer',   'CS2304', 'CSE',   5),
    ('Vikram Bose',  'CV2305', 'CIVIL', 1);

INSERT INTO subjects (code, name, credits) VALUES
    ('CS501', 'Operating Systems',      4),
    ('CS502', 'Database Management',    4),
    ('CS503', 'Computer Networks',      3);

INSERT INTO results (student_id, gpa, grade, semester) VALUES
    (1, 9.1, 'A', 5),
    (2, 8.4, 'A', 3),
    (3, 7.6, 'B', 7),
    (4, 6.9, 'C', 5),
    (5, 5.2, 'C', 1);

INSERT INTO enrollments (student_id, subject_id, enrolled_on) VALUES
    (1, 1, '2024-01-10'), (1, 2, '2024-01-10'), (1, 3, '2024-01-10'),
    (2, 1, '2024-01-10'), (2, 2, '2024-01-10'),
    (3, 2, '2024-01-10'), (3, 3, '2024-01-10'),
    (4, 1, '2024-01-10'), (4, 2, '2024-01-10'),
    (5, 3, '2024-01-10');

INSERT INTO marks_detail (student_id, subject_id, marks) VALUES
    (1, 1, 91), (1, 2, 88), (1, 3, 85),
    (2, 1, 84), (2, 2, 79),
    (3, 2, 76), (3, 3, 72),
    (4, 1, 69), (4, 2, 65),
    (5, 3, 52);
