#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER petal_admin WITH PASSWORD 'mysecretpassword';
    CREATE DATABASE petal;
    GRANT ALL PRIVILEGES ON DATABASE petal TO petal_admin;
EOSQL

psql -v ON_ERROR_STOP=1 --username "petal_admin" --dbname "petal" <<-EOSQL
    CREATE TABLE functions (
        id INT NOT NULL,
        function VARCHAR (50) NOT NULL
    );

    INSERT INTO functions (id, function)
    VALUES
        (1, 'Reduce drag'),
        (2, 'Absorb shock'),
        (3, 'Dissipate heat'),
        (4, 'Increase lift'),
        (5, 'Remove particles from a surface');
EOSQL