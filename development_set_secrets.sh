#!/bin/bash

set -euo pipefail


function usage {
    echo "This initializes all secrets for an development setup. If you want to use it for an production environment, please review the commands and adapt it."
    echo "Usage:"
    echo "${0}"
    echo "        [-h | --help] Print this help"
}

for i in "$@"
do
case $i in
   -h|--help)
    usage
    exit
    ;;

    *)
    echo "Unknown option $i. Ignoring it." > /dev/stderr
    ;;
esac
done

# Create docker secrets needed for the services
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-postgres-password -
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-redis-password -
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-secret-key -
 echo -n ' ' | docker secret create inyoka-akismet-key -
# note the space at the start of the command to prevent the secret in the shell history
 echo -n 'https://examplePublicKey@localhost/0' | docker secret create inyoka-sentry-dsn -


# configure used domains
echo -n 'ubuntuusers.localhost' | docker config create inyoka-base-domain -
echo -n 'media.ubuntuusers.localhost' | docker config create inyoka-media-domain -
echo -n 'static.ubuntuusers.localhost' | docker config create inyoka-static-domain -


# Provide an email (used by caddy for ACME)
echo -n 'inyoka@localhost' | docker config create caddy-email -
