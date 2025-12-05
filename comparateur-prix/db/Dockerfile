#On part de l'image officielle de mysql
FROM mysql:5.7

#Variable d'environnement
ENV MYSQL_DATABASE = Produits
ENV MYSQL_ROOT_PASSWORD = toto

COPY init.sql /docker-entrypoint_initdb.d/
