# PeTaL (Periodic Table of Life)

The Periodic Table of Life (PeTaL, pronounced petal) is a design tool aimed at allowing users to seemlesly move from ideas (from nature or other sources) to design.

PeTaL is comprised of multiple interconnected services. This repository is for the PostgreSQL database server. There are other repositories for the [ReactJS web front end client](https://github.com/nasa/PeTaL), [API](https://github.com/nasa/petal-api) and [Labeller](https://github.com/nasa/petal-labeller).

## Getting started

https://hub.docker.com/_/postgres

https://towardsdatascience.com/local-development-set-up-of-postgresql-with-docker-c022632f13ea

`docker pull postgres`
```docker run -d \
    --name petal-db \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -d \
    -v ~/Documents/localwrk/git/petal-db/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d \
    -p 5432:5432 \
    postgres```

`docker exec -it petal-db bash`
`psql -h localhost -U postgres`
`\l`
`\c petal`
`select * from wikipedia_label;`

`docker inspect petal-db -f "{{json .NetworkSettings.Networks }}"`