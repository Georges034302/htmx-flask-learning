-- Employee database setup script
--
-- Recommended usage for SQLite:
--   sqlite3 employees.db < data/employee_db_setup.sql
--
-- For PostgreSQL/MySQL, create/select the database first, then run this script.
-- Example (PostgreSQL):
--   CREATE DATABASE employee_db;
--   \c employee_db

BEGIN TRANSACTION;

DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL
);

INSERT INTO employees (id, name, department) VALUES
    (1, 'Alice', 'IT'),
    (2, 'Bob', 'HR'),
    (3, 'Charlie', 'Finance'),
    (4, 'David', 'IT'),
    (5, 'Emma', 'Marketing'),
    (6, 'Frank', 'Security'),
    (7, 'Grace', 'IT'),
    (8, 'Helen', 'Finance'),
    (9, 'Ian', 'HR'),
    (10, 'Jack', 'Marketing'),
    (11, 'Karen', 'IT'),
    (12, 'Leo', 'Security');

COMMIT;
