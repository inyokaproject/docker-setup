FROM python:3.8.13-slim-bullseye AS inyoka_base
# 3.9 causes problems with feedparser
# 3.10 not offically supported by django 2.2

# ARG 'is not persisted in the final image' see https://docs.docker.com/engine/reference/builder/#env
ARG DEBIAN_FRONTEND=noninteractive
# from https://docs.docker.com/samples/django/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y --no-install-recommends libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev uuid-dev libfreetype6-dev libpq-dev build-essential libpq-dev libffi-dev wget libmagic1

# inyoka
COPY inyoka /inyoka/code
WORKDIR /inyoka/code
RUN python3 -m venv /inyoka/venv
RUN /inyoka/venv/bin/pip install --no-cache-dir --upgrade pip
RUN /inyoka/venv/bin/pip install --require-hashes --no-cache-dir -r extra/requirements/development.txt

# theme
COPY theme-ubuntuusers /inyoka/theme
RUN sh -c 'cd /inyoka/theme && /inyoka/venv/bin/python setup.py develop'

# remove previously collected statics (could be also symlinks)
RUN rm -rf /inyoka/code/inyoka/static-collected



# only install node packages in an intermediate container
# the build statics will be copied in the next step
# for Docker multistage-build see https://docs.docker.com/develop/develop-images/multistage-build/
FROM inyoka_base AS inyoka_with_node
WORKDIR /inyoka/theme
RUN apt-get install -y --no-install-recommends nodejs npm
RUN npm ci
RUN npm run all
WORKDIR /inyoka/code
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
