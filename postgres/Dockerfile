FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/
COPY data/lineas.csv /docker-entrypoint-initdb.d/lineas.csv
COPY data/paradas.csv /docker-entrypoint-initdb.d/paradas.csv