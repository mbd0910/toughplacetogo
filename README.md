Rebuild and start your containers using Docker Compose and an environment file:

```shell
docker-compose up --env-file .env --build
```

Stop and remove containers

```shell
docker-compose down
```

with volumes as well

```shell
docker-compose down -v
```
