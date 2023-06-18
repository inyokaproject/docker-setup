#!/bin/bash

set -euo pipefail

tag=staging
inyoka_version=$(git -C inyoka/ describe --tags)--theme-ubuntuusers$(git -C theme-ubuntuusers/ describe --tags)


function usage {
    echo "This is a little bash helper script to avoid typing very long command lines."
    echo "Usage:"
    echo "${0}"
    echo "        [-p | --prod | --production] Build images for production environment. Otherwise images for staging are built."
    echo "        [-h | --help] Print this help"
}

for i in "$@"
do
case $i in
    -p|--prod|--production)
    tag=latest
    ;;

   -h|--help)
    usage
    exit
    ;;

    *)
    echo "Unknown option $i. Ignoring it." > /dev/stderr
    ;;
esac
done


# Build the inyokaproject image
docker build --pull -t inyokaproject:"${inyoka_version}" -t inyokaproject:"${tag}" -t git.ubuntu-eu.org/ubuntuusers/inyokaproject:"${inyoka_version}" -t git.ubuntu-eu.org/ubuntuusers/inyokaproject:"${tag}" .

# Build the custom caddy image (that includes the static files for inyoka)
docker build -t caddy-inyoka:"${inyoka_version}" -t caddy-inyoka:"${tag}" -t git.ubuntu-eu.org/ubuntuusers/caddy-inyoka:"${inyoka_version}" -t git.ubuntu-eu.org/ubuntuusers/caddy-inyoka:"${tag}" --file Dockerfile_caddy .
