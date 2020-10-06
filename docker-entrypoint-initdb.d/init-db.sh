#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER petal_admin WITH PASSWORD 'mysecretpassword';
    CREATE DATABASE petal;
    GRANT ALL PRIVILEGES ON DATABASE petal TO petal_admin;
EOSQL

psql -v ON_ERROR_STOP=1 --username "petal_admin" --dbname "petal" <<-EOSQL
    CREATE TABLE Label (
        id INT UNIQUE NOT NULL,
        label VARCHAR (50) NOT NULL
    );

    INSERT INTO Label (id, label)
    VALUES
        (1, 'Reduce drag'),
        (2, 'Absorb shock'),
        (3, 'Dissipate heat'),
        (4, 'Increase lift'),
        (5, 'Remove particles from a surface');

    CREATE TABLE Wikipedia_Article (
        id INT UNIQUE NOT NULL
    );

    INSERT INTO Wikipedia_Article (id)
    VALUES
        (7681471),
        (10692973),
        (508889),
        (64922341),
        (12760348),
        (12436171),
        (36533086),
        (64923006),
        (345410),
        (484282),
        (506116),
        (12635570),
        (12462709),
        (1459299),
        (30203705),
        (391347),
        (6550154),
        (413741),
        (413732),
        (6024329),
        (508847),
        (12469183),
        (429433),
        (12292601),
        (6569805),
        (4470304);

    CREATE TABLE Wikipedia_Label (
        label_id INT NOT NULL,
        article_id INT NOT NULL
    );

    INSERT INTO Wikipedia_Label (label_id, article_id)
    VALUES
        (1,7681471),
        (1,10692973),
        (1,508889),
        (1,64922341),
        (1,12760348),
        (1,12436171),
        (2,36533086),
        (2,64923006),
        (2,345410),
        (2,484282),
        (2,506116),
        (2,12635570),
        (3,12462709),
        (3,1459299),
        (3,30203705),
        (3,391347),
        (3,6550154),
        (4,413741),
        (4,413732),
        (4,6024329),
        (4,508847),
        (4,12469183),
        (5,429433),
        (5,12292601),
        (5,6569805),
        (5,4470304); 
EOSQL