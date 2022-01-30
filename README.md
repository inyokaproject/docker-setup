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

Start the stack

```
docker stack deploy -c docker-compose.yaml inyoka
```

Show the status of the services

```
docker service ls
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

Oter notes
----------

 * "Where is Docker actually storing my data when I use a named volume?"  
   `docker volume inspect <volume-name>`
