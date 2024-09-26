# Tough Place To Go

Football pundits frequently say that the team that is bottom of their respective league is a "tough place to go",
despite all evidence pointing to it being the easiest away game of the season. For some reason this phrase has always 
struck a chord with me, and it has therefore become the name of the home of my football analyses.

WIP:
- League Tables always lie. Adding more context to football league tables to give an indication of whether we can trust
it yet.

## Old Docker instructions

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
