-- Employee database setup script — MySQL 8 compatible
--
-- Local manual usage:
--   mysql -u root -p < data/employee_db_setup.sql
--
-- Docker usage (automatic):
--   Mount this file into the MySQL container init directory:
--   ./data/employee_db_setup.sql:/docker-entrypoint-initdb.d/employee_db_setup.sql
--   The mysql:8 image runs all *.sql files in that directory on first start.
--
-- SQLite usage (early development modules only):
--   sqlite3 employees.db < data/employee_db_setup.sql
--   Note: Remove the CREATE DATABASE / USE / ENGINE / COLLATE lines first.

CREATE DATABASE IF NOT EXISTS employees_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE employees_db;

DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    department  VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO employees (name, department) VALUES
    ('Alice',   'IT'),
    ('Bob',     'HR'),
    ('Charlie', 'Finance'),
    ('David',   'IT'),
    ('Emma',    'Marketing'),
    ('Frank',   'Security'),
    ('Grace',   'IT'),
    ('Helen',   'Finance'),
    ('Ian',     'HR'),
    ('Jack',    'Marketing'),
    ('Karen',   'IT'),
    ('Leo',     'Security');
