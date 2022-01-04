#!/bin/bash

cd /inyoka/theme
~/.venvs/inyoka/bin/python setup.py develop

npm install
npm run all
