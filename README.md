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
```docker build -t inyokaproject .```

Create docker secrets needed for the services

```
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-postgres-password -
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-redis-password -
openssl rand -base64 32 | tr -d '\n' | docker secret create inyoka-secret-key -
docker secret create inyoka-akismet-key /path/to/file_with_secret/
# note the space at the start of the command to prevent the secret in the shell history
 echo -n 'https://examplePublicKey@localhost/0' | docker secret create inyoka-sentry-dsn -
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

To publish the port of the web worker

```
docker service update --publish-add published=80,target=8000 inyoka_inyoka-worker
```

Run migrations (works only on the same machine, where the container runs)

```
docker exec -it <container> /root/.venvs/inyoka/bin/python manage.py migrate
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




for a development setup run

```docker stack deploy --compose-file docker-compose.yaml --compose-file docker-development.yml inyoka-dev```


Other notes
-----------

 * "Where is Docker actually storing my data when I use a named volume?"  
   `docker volume inspect <volume-name>`
