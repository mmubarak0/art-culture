-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS anc_dev_db;
CREATE USER IF NOT EXISTS 'anc_dev'@'localhost' IDENTIFIED BY 'artnculture';
GRANT ALL PRIVILEGES ON `anc_dev_db`.* TO 'anc_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'anc_dev'@'localhost';
FLUSH PRIVILEGES;
