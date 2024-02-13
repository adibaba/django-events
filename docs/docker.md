# Docker - Documentation - Django Event Management

- Dockerfiles are in sub-directory [Docker](../Docker)
- Some commands below are based on [Podman](https://podman.io/) (Microsoft Windows), but they are similar to [Docker](https://www.docker.com/) commands.
- Dockerfiles are based on [Debian version](https://en.wikipedia.org/wiki/Debian_version_history) 12 "Bookworm" (June 2023) and Python 3.11.4: [python:3.11.4-slim-bookworm](https://hub.docker.com/layers/library/python/3.11.4-slim-bookworm/images/sha256-0275089b5b654bb33931fc239a447db9fdd1628bc9d1482788754785d6d9e464?context=explore).

## Eventslite - Simple container using SQlite

- Note: This will copy the files of the current directory, including the currently used SQLite database. Maybe you want to clean up your code first.
- Build an image from the [Dockerfile-SQLite](../Docker/Dockerfile-SQLite) (also copies files).
  It installs requirements_dev.txt, copies files and runs migrate:  
  `podman build --tag eventslite --file Docker/Dockerfile-SQLite ./`
- Create and run a new container from the image:  
  `podman run --name eventslite --detach --interactive --tty --publish 8000:8000 eventslite`
- Import example data:  
  `podman exec eventslite python manage.py loaddata events/fixtures/examples/0001_user.xml events/fixtures/examples/0002_person.xml events/fixtures/examples/0003_event.xml events/fixtures/examples/0004_registration.xml`
- Start server in interactive bash:  
  `podman exec --interactive --tty eventslite bash`  
  - `python manage.py runserver 0.0.0.0:8000`  
- Stop server in interactive bash:  
  - Press [ctrl]+[c] and type `exit`
- Stop the container:  
  `podman stop eventslite`

## Compose - Container using Postgres

- Create and start containers from the [Dockerfile](../Docker/Dockerfile).
  It installs requirements_prod.txt, copies files and runs migrate:  
  `podman-compose --file Docker/docker-compose.yml --project-name events up --detach`
- Passwords for the database and superuser are set via environment variables in [docker-compose.yml](../Docker/docker-compose.yml).
- To stop and remove containers, use `down`
- To (re-) build services, use `build`

## Commands

- [Docker CLI reference](https://docs.docker.com/engine/reference/run/),
  [Podman commands](https://docs.podman.io/en/latest/Commands.html)
- [Docker compose CLI reference](https://docs.docker.com/compose/reference/),
  [Podman compose command](https://docs.podman.io/en/latest/markdown/podman-compose.1.html)
- `podman images --all` List all images
- `podman rmi events` Remove events image
- `podman rmi --all` Remove all images
- `podman ps --all` List all containers
- `podman rm events` Remove containers events
- `podman rm --all` Remove all containers
- Clean up:  
  `podman rmi events_events`  
  `podman image prune`  
  `podman volume rm events_postgres`  
  `podman volume prune`

## Python settings

```python
# Ensure Python output is logged to the terminal, making it possible to monitor Django logs in realtime 
# https://www.nileshdalvi.com/blog/dockerize-django-app/
#
# Force the stdout and stderr streams to be unbuffered
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED 1
```

## Postgres image

- Docker Hub
  - [postgres](https://hub.docker.com/_/postgres/)
  Website also describes *environment variables* and *compose* usage
  - [postgres:16.0-bookworm](https://hub.docker.com/_/postgres/tags?page=1&name=16.0-bookworm)
