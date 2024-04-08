-- Create the database
CREATE DATABASE riff;

-- Create an admin user for our app to use
CREATE USER riff_admin WITH PASSWORD 'password';

-- Give that user permissins to manage the database:
GRANT ALL PRIVILEGES ON DATABASE riff TO riff_admin;