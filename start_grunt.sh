#!/bin/bash
cd /srv/www/theme-ubuntuusers
source ~/.venvs/inyoka/bin/activate
npm install
./node_modules/grunt-cli/bin/grunt watch
