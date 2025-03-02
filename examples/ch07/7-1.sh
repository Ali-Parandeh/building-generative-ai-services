docker run -p 5432:5432  \
	-e POSTGRES_USER=fastapi \
	-e POSTGRES_PASSWORD=mysecretpassword \
	-e POSTGRES_DB=backend_db \
	-e PGDATA=/var/lib/postgresql/data \
  -v "$(pwd)"/dbstorage:/var/lib/postgresql/data \
  postgres:latest