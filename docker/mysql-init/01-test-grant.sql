-- The application user can create only its isolated Django test database.
-- MySQL is not exposed on a host port. No root credentials enter the web service.
GRANT ALL PRIVILEGES ON test_festival.* TO 'festival'@'%';
