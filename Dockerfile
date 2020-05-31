FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y --no-install-recommends nodejs libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev uuid-dev libfreetype6-dev libpq-dev build-essential libpq-dev libffi-dev python2.7 libpython2.7-dev wget npm libmagic1

# ---------- prepare inyoka ---------

COPY inyoka /srv/www/inyoka

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python2 get-pip.py
RUN pip install virtualenv

RUN mkdir -p ~/.venvs/
RUN virtualenv --python=python2 ~/.venvs/inyoka

RUN bash -c 'cd /srv/www/inyoka && source ~/.venvs/inyoka/bin/activate && pip install -r extra/requirements/development.txt'
RUN bash -c 'cd /srv/www/inyoka && source ~/.venvs/inyoka/bin/activate'

COPY start_inyoka.sh /start_inyoka.sh

## ---------- prepare theme ---------
#
COPY theme-ubuntuusers /srv/www/theme-ubuntuusers
#
RUN bash -c 'cd /srv/www/theme-ubuntuusers && source ~/.venvs/inyoka/bin/activate && python setup.py develop && npm install && ./node_modules/grunt-cli/bin/grunt'

COPY start_grunt.sh /start_grunt.sh

## ----------------------------------

VOLUME ["/srv/www/inyoka", "/srv/www/theme-ubuntuusers"]
