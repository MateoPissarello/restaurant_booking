### Correr el contenedor de la db
docker-compose up -d


### Hacer migraciones

alembic revision --autogenerate -m "mensaje"
alembic upgrade heads