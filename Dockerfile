FROM docker.io/library/python:3.12.3-slim-bookworm AS inyoka_base

LABEL org.opencontainers.image.source=https://github.com/inyokaproject/docker-setup
LABEL org.opencontainers.image.description="Inyoka container image"
LABEL org.opencontainers.image.licenses=BSD-3-Clause
LABEL org.opencontainers.image.title=Inyoka
LABEL org.opencontainers.image.vendor="Inyoka Team"

# ARG 'is not persisted in the final image' see https://docs.docker.com/engine/reference/builder/#env
ARG DEBIAN_FRONTEND=noninteractive
# from https://docs.docker.com/samples/django/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y --no-install-recommends libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev uuid-dev libfreetype6-dev libpq-dev build-essential libpq-dev libffi-dev libmagic1 postgresql-client

# inyoka
COPY inyoka /inyoka/code
WORKDIR /inyoka/code
RUN python3 -m venv /inyoka/venv
RUN /inyoka/venv/bin/pip install --no-cache-dir --upgrade pip
RUN /inyoka/venv/bin/pip install --no-deps --require-hashes --no-cache-dir -r extra/requirements/production.txt
RUN /inyoka/venv/bin/pip install -e /inyoka/code

# theme
COPY theme-ubuntuusers /inyoka/theme
RUN /inyoka/venv/bin/pip install -e /inyoka/theme

# remove previously collected statics (could be also symlinks)
RUN rm -rf /inyoka/code/inyoka/static-collected



# only install node packages in an intermediate container
# the build statics will be copied in the next step
# for Docker multistage-build see https://docs.docker.com/develop/develop-images/multistage-build/
FROM inyoka_base AS inyoka_with_node

ARG INYOKA_THEME=inyoka_theme_ubuntuusers

WORKDIR /inyoka/theme
RUN apt-get install -y --no-install-recommends nodejs npm
RUN npm ci
RUN npm run all

WORKDIR /inyoka/code
# create small temporary development settings file, so collectstatic can run
RUN printf "from inyoka.default_settings import *\nINSTALLED_APPS += ('${INYOKA_THEME}',)" > development_settings.py
RUN /inyoka/venv/bin/python manage.py collectstatic --noinput



FROM inyoka_base AS inyoka_with_statics
COPY --from=inyoka_with_node /inyoka/code/inyoka/static-collected /inyoka/code/inyoka/static-collected/

# setup own inyoka user instead of root
RUN touch /inyoka/code/celery.log /inyoka/code/inyoka.log
RUN mkdir -p /volume/celerybeat-schedule/ /srv/www/media
RUN groupadd --gid 998 --system inyoka
RUN useradd --system --no-create-home --no-log-init --gid inyoka --groups inyoka --uid 998 inyoka
RUN chown inyoka:inyoka /inyoka/code/celery.log /inyoka/code/inyoka.log /volume/celerybeat-schedule/ /srv/www/media
USER inyoka
