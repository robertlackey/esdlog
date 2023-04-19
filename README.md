# This is not a production-ready application
 
**Requires Docker and Docker Compose**

Add .env file with the following values
```
POSTGRES_DB=esdlog
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_URL=postgres
```

Start the app
```
chmod +x startup.sh
./startup.sh
```

Stop the containers
```
docker-compose down
```
