-- Prepares the MySQL server for this project

-- Create the testing database if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the testing user if it does not exist, with password
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the testing database to the testing user
GRANT ALL PRIVILEGES ON `hbnb_test_db`.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privileges on performance_schema (optional, for monitoring)
GRANT SELECT ON `performance_schema`.* TO 'hbnb_test'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
