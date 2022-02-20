Run inyoka and themes in docker
============================

requirements
-------------

 * [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu)
 * [docker compose](https://docs.docker.com/compose/cli-command/#install-on-linux) (mind the missing `-`. `docker-compose` is another binary and would be also available in Ubuntu universe. However, there it is outdated. The Docker PPA seems to not include `docker-compose` neither `docker compose` (yet)...)

prepare
-------

Inside a directory of your choice run
```
git clone git@github.com:inyokaproject/docker-setup.git . # take note of the '.'
git clone git@github.com:inyokaproject/inyoka.git
git clone git@github.com:inyokaproject/theme-ubuntuusers.git
```

Inside this directory you can run more commands:


 * check whether docker swarm is alrady enabled on your machine  
  `docker system info | grep Swarm`
 * if not, enable it via `docker swarm init`

build the inyokaproject image
```docker build -t inyokaproject .```

Create docker secrets needed for the services

```
openssl rand -base64 32 | docker secret create inyoka-postgres-password -
openssl rand -base64 32 | docker secret create inyoka-secret-key -
docker secret create inyoka-akismet-key /path/to/file_with_secret/
# note the space at the start of the command to prevent the secret in the shell history
 echo -n 'https://examplePublicKey@localhost/0' | docker secret create inyoka-sentry-dsn -
```

Start the stack

```
docker stack deploy -c docker-compose.yaml inyoka
```

Show the status of the services

```
docker service ls
```

TODO: To publish the port of the web worker

```
docker service update --publish-add published=8000,target=8000 inyoka_inyoka-worker
```


Remove the stack

```
docker stack rm inyoka
```

View logs

```
docker service logs <service name from service ls>
```

 * Add `-f` to follow for new entries

TODO
prepare inyoka config:

```cp development_settings.py inyoka/```

build docker image:

```docker compose build```

run in foreground

```docker compose up```

run in background

```docker compose up -d```

show logs from running in background

```docker compose logs```

stop running in background

```docker compose down```


for a development setup run

```docker compose -f docker-compose.yaml -f docker-development.yml up```

Other notes
-----------

 * "Where is Docker actually storing my data when I use a named volume?"  
   `docker volume inspect <volume-name>`
