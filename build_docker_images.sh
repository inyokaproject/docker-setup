#!/bin/bash

set -euo pipefail

tag=staging
inyoka_version=$(git -C inyoka/ describe --tags)
registry_path="git.ubuntu-eu.org/ubuntuusers" # no / at the end here
docker_build_target="inyoka"

function usage {
    echo "This is a little bash helper script to avoid typing very long command lines."
    echo "Usage:"
    echo "${0}"
    echo "        [-p | --prod | --production] Build images for production environment. Otherwise images for staging are built."
    echo "        [--theme] Build images with a customized theme."
    echo "        [-h | --help] Print this help"
}

for i in "$@"
do
case $i in
    -p|--prod|--production)
    tag=latest
    ;;

    --theme)
    docker_build_target="inyoka_custom_theme"
    inyoka_version="${inyoka_version}--theme$(git -C theme/ describe --tags)"
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
docker build --pull --target "${docker_build_target}" -t inyokaproject:"${inyoka_version}" -t inyokaproject:"${tag}" -t "${registry_path}"/inyokaproject:"${inyoka_version}" -t "${registry_path}"/inyokaproject:"${tag}" .

# Build the custom caddy image (that includes the static files for inyoka)
docker build -t caddy-inyoka:"${inyoka_version}" -t caddy-inyoka:"${tag}" -t "${registry_path}"/caddy-inyoka:"${inyoka_version}" -t "${registry_path}"/caddy-inyoka:"${tag}" --file Dockerfile_caddy --build-context git.ubuntu-eu.org/ubuntuusers/inyokaproject=docker-image://inyokaproject:${tag} .
