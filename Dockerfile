# global build arguments → https://docs.docker.com/build/building/variables/#scoping
ARG INYOKA_THEME_APP=inyoka_theme_ubuntuusers


FROM docker.io/library/python:3.12.6-slim-bookworm AS inyoka_base

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

# remove previously collected statics (could be also symlinks)
RUN rm -rf /inyoka/code/inyoka/static-collected

# setup own inyoka user instead of root
RUN touch /inyoka/code/celery.log /inyoka/code/inyoka.log
RUN mkdir -p /volume/celerybeat-schedule/ /srv/www/media
RUN groupadd --gid 998 --system inyoka
RUN useradd --system --no-create-home --no-log-init --gid inyoka --groups inyoka --uid 998 inyoka
RUN chown inyoka:inyoka /inyoka/code/celery.log /inyoka/code/inyoka.log /volume/celerybeat-schedule/ /srv/www/media


FROM inyoka_base AS inyoka_base_theme

# theme
COPY theme /inyoka/theme
RUN /inyoka/venv/bin/pip install -e /inyoka/theme


# only install node packages in an intermediate container
# the build statics will be copied in the next step
# for Docker multistage-build see https://docs.docker.com/develop/develop-images/multistage-build/
FROM inyoka_base AS inyoka_with_node

RUN apt-get install -y --no-install-recommends nodejs npm

# build statics inside Inyoka
RUN npm ci
RUN npm run all

FROM inyoka_with_node AS inyoka_collected
ARG DJANGO_SETTINGS_MODULE="tests.settings.base"
RUN /inyoka/venv/bin/python manage.py collectstatic --noinput

FROM inyoka_with_node AS inyoka_theme_with_node

COPY --from=inyoka_base_theme /inyoka/theme /inyoka/theme/
COPY --from=inyoka_base_theme /inyoka/venv /inyoka/venv/

ARG INYOKA_THEME_APP

# build statics theme
WORKDIR /inyoka/theme
RUN npm ci
RUN npm run all

WORKDIR /inyoka/code
# minimal development settings, so collectstatic allows overwrites
COPY <<EOF development_settings.py
from inyoka.default_settings import *
INSTALLED_APPS += ('${INYOKA_THEME_APP}',)

from os.path import join
THEME_PATH = '/inyoka/theme/${INYOKA_THEME_APP}'
STATICFILES_DIRS = [join(THEME_PATH, 'static'), ] + STATICFILES_DIRS
#TEMPLATES[1]['DIRS'].insert(0, join(THEME_PATH, 'jinja2'))
EOF
RUN /inyoka/venv/bin/python manage.py collectstatic --noinput


FROM inyoka_base AS inyoka
COPY --from=inyoka_collected /inyoka/code/inyoka/static-collected /inyoka/code/inyoka/static-collected/
# use own inyoka user instead of root
USER inyoka


FROM inyoka_base_theme AS inyoka_custom_theme
ARG INYOKA_THEME_APP
ENV INYOKA_THEME_APP=$INYOKA_THEME_APP
COPY --from=inyoka_theme_with_node /inyoka/code/inyoka/static-collected /inyoka/code/inyoka/static-collected/
# use own inyoka user instead of root
USER inyoka
