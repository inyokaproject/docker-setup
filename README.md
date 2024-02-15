Run inyoka with theme in docker
===============================

requirements
-------------

 * [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu)

prepare
-------

 * check whether docker swarm is alrady enabled on your machine  
  `docker system info | grep Swarm`
 * if not, enable it via `docker swarm init`

Inside a directory of your choice clone the required repositories
```
git clone git@github.com:inyokaproject/docker-setup.git . # take note of the '.'
git clone git@github.com:inyokaproject/inyoka.git
git clone git@github.com:inyokaproject/theme-ubuntuusers.git
```

Inside this directory you can run more commands:

Build the inyokaproject image
```
docker build --pull -t inyokaproject:$(git -C inyoka/ describe --tags)--theme-ubuntuusers$(git -C theme-ubuntuusers/ describe --tags) -t inyokaproject:latest .
```

Build the custom caddy image (that includes the static files for inyoka)
```
docker build -t caddy-inyoka:$(git -C inyoka/ describe --tags)--theme-ubuntuusers$(git -C theme-ubuntuusers/ describe --tags) -t caddy-inyoka:latest --file Dockerfile_caddy .
```

Create docker secrets needed for the services

```
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-postgres-password -
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-redis-password -
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-secret-key -
docker secret create inyoka-akismet-key /path/to/file_with_secret/
# note the space at the start of the command to prevent the secret in the shell history
 echo -n 'https://examplePublicKey@localhost/0' | docker secret create inyoka-sentry-dsn -
```

Provide an email (used by caddy for ACME)

```
echo -n 'inyoka@localhost' | sudo docker config create caddy-email -
```

Change the domains according to your needs:

```
echo -n 'ubuntuusers.de' | docker config create inyoka-base-domain -
echo -n 'media-cdn.ubuntu-de.org' | docker config create inyoka-media-domain -
echo -n 'static-cdn.ubuntu-de.org' | docker config create inyoka-static-domain -
```


Review the prepared inyoka config files, if everything fits your needs (f.e. the maximum cache sizes to the server's physical amount of RAM).

Start the stack

```
docker stack deploy -c docker-compose.yaml inyoka
```

Show the status of the services

```
docker service ls
```

To publish the ports of the web server

```
docker service update --publish-add published=80,target=80 --publish-add published=443,target=443 --publish-add published=443,target=443,protocol=udp inyoka_caddy
```

Run migrations (works only on the same machine, where the container runs)

```
docker exec -it <container id> /inyoka/venv/bin/python manage.py migrate
```

You can get the container id via `docker container ls`.


Remove the stack

```
docker stack rm inyoka
```

View logs

```
docker service logs <service name from service ls>
```

 * Add `-f` to follow for new entries



Development setup
-----------------

For development you have to install docker compose via the package `docker-compose-plugin` in the PPA.

Set the docker config values like for production. However, adapt the domain name to end with `.localhost`. Some example values:

```
echo -n 'ubuntuusers.localhost' | docker config create inyoka-base-domain -
echo -n 'media.ubuntuusers.localhost' | docker config create inyoka-media-domain -
echo -n 'static.ubuntuusers.localhost' | docker config create inyoka-static-domain -
echo -n 'inyoka@localhost' | docker config create caddy-email -
```


Create docker secrets needed for the services

```
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-postgres-password -
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-redis-password -
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-secret-key -
docker secret create inyoka-akismet-key /path/to/file_with_secret/
# note the space at the start of the command to prevent the secret in the shell history
 echo -n 'https://examplePublicKey@localhost/0' | docker secret create inyoka-sentry-dsn -
```

Login to Inyoka-Docker Source

if you don't build the container on your system and have access to the inyoka-contianer repository, you have to login first:

```
docker login https://git.ubuntu-eu.org
```

To create a development setup run

```
# needed as docker stack does not overwrite 'command' (instead the one from docker-development gets appendeded), see https://github.com/docker/cli/issues/1651#issuecomment-467759678
docker compose -f docker-compose.yaml -f docker-development.yml config | tail -n +2 | { echo 'version: "3.8"'; cat -; } | docker stack deploy -c - inyoka-dev
docker service update --publish-add published=80,target=8000 --publish-add published=8443,target=443 inyoka-dev_caddy
```

You should now be able to visit `ubuntuusers.localhost:8000` in your browser.

 * To create some testdata execute  
   ```docker exec -it <container> /inyoka/venv/bin/python ./make_testdata.py```
 * To create a superuser account named `admin` execute  
   ```docker exec -it <container> /inyoka/venv/bin/python manage.py create_superuser --username admin --email 'admin@localhost'```

 * E-Mail logs can be seen via `docker service logs inyoka-dev_smtpd`

To get the local TLS root certifcate of caddy execute

```
docker exec -it <caddy container id> cat /data/caddy/pki/authorities/local/root.crt > caddy_local_root.crt
```

It is recommended to use a separate browser profile only for local development. In this separate profile you can import the root certificate.
The local root CA will not change as long as the caddy volumes are the same.

As an alternative, you can also trust all `*.ubuntuusers.localhost` domains manually.
However, the leaf certifcates seem to be only valid for one day.

Other notes
-----------

 * "Where is Docker actually storing my data when I use a named volume?"  
   `docker volume inspect <volume-name>`
 * [Supported Debian releases](https://wiki.debian.org/DebianReleases#Production_Releases)
 * [Alpine releases](https://alpinelinux.org/releases/)
 * [Caddy releases](https://github.com/caddyserver/caddy/releases) ([Feed](https://github.com/caddyserver/caddy/releases.atom))
 * [Python releases](https://www.python.org/downloads/) ([Feed](https://github.com/python/cpython/releases.atom))
 * [Redis releases](https://github.com/redis/redis/releases) ([Feed](https://github.com/redis/redis/releases.atom))
 * [Supported postgreSQL releases](https://www.postgresql.org/support/versioning/) ([Feed](https://www.postgresql.org/news/pgsql.rss))
