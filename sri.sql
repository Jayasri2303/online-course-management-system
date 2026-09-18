SHOW DATABASES;
USE course_management_system;
SELECT DATABASE();

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    instructor_id INT,
    FOREIGN KEY (instructor_id)
    REFERENCES users(user_id)
);

CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    UNIQUE(student_id, course_id)
);

CREATE TABLE materials (
    material_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT,
    title VARCHAR(100),
    content VARCHAR(1000),
    FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
);

CREATE TABLE progress (
    progress_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    progress_percentage INT DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    UNIQUE(student_id, course_id)
);

SHOW TABLES;

