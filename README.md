# A backend for a personal app

This repository contains a playground for a python-based backend
with Flask, isolated in a docker container. Not sure what it will do yet! :)

## Running the latest image version

```bash
python3 ./scripts/dev.py start
```

## Running the flask backend outside docker

```bash
python3 ./image/app.py
```

## Building the docker image locally

```bash
python3 ./scripts/dev.py build
```

## Open TODOs

* Add proper logging
