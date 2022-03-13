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



Development setup
-----------------

You have to install docker compose via the package `docker-compose-plugin` in the PPA.

To create a development setup run

```
# needed as docker stack does not overwrite 'command' (instead the one from docker-development gets appendeded), see https://github.com/docker/cli/issues/1651#issuecomment-467759678
docker compose -f docker-compose.yaml -f docker-development.yml config | tail -n +2 | { echo 'version: "3.8"'; cat -; } | docker stack deploy -c - inyoka-dev
docker service update --publish-add published=8000,target=8000 inyoka-dev_inyoka-worker
```

You should now be able to visit `ubuntuusers.localhost:8000` in your browser.

 * To create some testdata execute  
   ```docker exec -it <container> /root/.venvs/inyoka/bin/python ./make_testdata.py```
 * To create a superuser account named `admin` execute  
   ```docker exec -it <container> /root/.venvs/inyoka/bin/python manage.py create_superuser --username admin --email 'admin@localhost'```

 * E-Mail logs can be seen via `docker service logs inyoka-dev_smtpd`

Other notes
-----------

 * "Where is Docker actually storing my data when I use a named volume?"  
   `docker volume inspect <volume-name>`
