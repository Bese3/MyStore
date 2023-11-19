-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS mystore_dev_db;
CREATE USER IF NOT EXISTS 'mystore_dev'@'localhost' IDENTIFIED BY 'mystore_dev_pwd';
GRANT ALL PRIVILEGES ON `mystore_dev_db`.* TO 'mystore_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'mystore_dev'@'localhost';
FLUSH PRIVILEGES;
