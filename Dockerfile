FROM python:3.8-slim-bullseye
# 3.9 causes problems with feedparser
# 3.10 not offically supported by django 2.2

# ARG 'is not persisted in the final image' see https://docs.docker.com/engine/reference/builder/#env
ARG DEBIAN_FRONTEND=noninteractive
# from https://docs.docker.com/samples/django/
ARG PYTHONDONTWRITEBYTECODE=1
ARG PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y --no-install-recommends nodejs libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev uuid-dev libfreetype6-dev libpq-dev build-essential libpq-dev libffi-dev python3-dev python3-venv wget npm libmagic1


# inyoka

COPY inyoka /inyoka/code
WORKDIR /inyoka/code

RUN python3 -m venv ~/.venvs/inyoka

RUN ~/.venvs/inyoka/bin/pip install --no-cache-dir --upgrade pip
RUN ~/.venvs/inyoka/bin/pip install --require-hashes --no-cache-dir -r extra/requirements/development.txt

COPY start_inyoka.sh /


# theme

COPY theme-ubuntuusers /inyoka/theme

RUN sh -c 'cd /inyoka/theme && ~/.venvs/inyoka/bin/python setup.py develop'

COPY build_statics.sh /
