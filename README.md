Run inyoka with theme in docker
===============================

Requirements
-------------

 * [Install docker](https://docs.docker.com/install/linux/docker-ce/ubuntu)

Enable Swarm
------------

 * check whether docker swarm is already enabled on your machine  
  `docker system info | grep Swarm`
 * if not, enable it via `docker swarm init`

Swarm is mainly used as it allows to use Docker secrets and configs.
Inyoka does not need multiple systems.

Clone repositories
------------------

Inside a directory of your choice clone the required repositories
```
git clone git@github.com:inyokaproject/docker-setup.git . # take note of the '.'
git clone git@github.com:inyokaproject/inyoka.git
```

If you want to use an own theme, clone it also:

```
git clone git@github.com:inyokaproject/theme-example.git ./theme
```

Review configuration files
--------------------------

Inyoka uses multiple components like a postgreSQL database or a cache.

Especially for production environments, review the prepared configuration files, if everything fits your needs.
Some examples:
 - Whether the maximum redis cache sizes fits to the server's amount of RAM.
 - Whether memory settings of postgreSQL fit to the server's amount of RAM.
 - In `production_settings.py`
   - `EMAIL_HOST` points to the right host, if you want to send mails.
   - Your preferred language is the default.
   - ...


Build container images
----------------------

If you have access to our container-registry and just want to use a pre-build image, you can skip this step. 

Otherwise, executed inside the docker-setup directory the script to build the Inyoka docker images:

```
./build_docker_images.sh
```

 - To tag the images for production environments Add the option `--production`. By default, they will be tagged for staging.
 - If you want to use an own theme, add `--theme`.

Create docker secrets
---------------------

Some services need secrets. An example script for development is provided.

 - for _development_ run `./development_set_secrets.sh`. The defaults should be fine here.
 - for _production_
   - Copy the script: `cp development_set_secrets.sh production_set_secrets.sh`
   - Check whether you want to use services like akismet or sentry. If you want to use it, adapt their secrets.
   - Change the `.localhost` domains to your custom ones
   - Adjust the email (used by caddy for ACME)
   - Run the customized script `./production_set_secrets.sh`

(As an alternative consider to set up the secrets via ansible's [community.docker.docker_secret](https://docs.ansible.com/ansible/latest/collections/community/docker/docker_secret_module.html))


Development: Adjust the user/group ids
--------------------------------------

(only for _development_ setups)

To get the current user and group id in your shell, execute
```
# user id
$ id -u
1000

# group id of user
$ id -g
100
```

Insert your specific values at the top of `docker-development.yml`. There is a `x-user:` section.

If you leave the default values, permission errors for the media volume are likely.


Login to Inyoka-Docker registry
-------------------------------

If you don't build the container on your system and have access to the inyoka-container repository, you have to log in first:  
```
docker login https://git.ubuntu-eu.org
```

Start the stack
---------------

 - for _development_  
```
docker stack deploy -c docker-compose.yaml -c docker-development.yml inyoka-dev --with-registry-auth --detach=false
```
For development container-images with tag `staging` are used.


 - for _production_  
```
docker stack deploy -c docker-compose.yaml inyoka --with-registry-auth --detach=false
```
For production the container-images with tag `latest` are used.


Service status
--------------

To view, whether all services are up and running, execute
```
docker service ls
```

or

```
docker stats
```

Run Migrations
--------------

Run database migrations (works only on the same machine, where the container runs)

```
docker exec -it <container id> /inyoka/venv/bin/python manage.py migrate
```

Either you use tab-completion or
get the container id from `docker container ls`.


Publish ports
-------------

To be able to access Inyoka, publish the ports of the caddy web server:

 - for _development_  
```
docker service update --publish-add published=80,target=80 --publish-add published=443,target=443 --publish-add published=443,target=443,protocol=udp inyoka-dev_caddy
```

 - for _production_  
```
docker service update --publish-add published=80,target=80 --publish-add published=443,target=443 --publish-add published=443,target=443,protocol=udp inyoka_caddy
```


You should now be able to visit your Inyoka instance in your browser.

 - for _development_ use the URL `ubuntuusers.localhost`.
   Most likely, for development you will see a certificate error, see the section below for details.
   You can use `curl -L --verbose -4 --insecure https://ubuntuusers.localhost/` to see, if a response is generated.
 - for _production_ use your custom URL


Create data
-----------

 * To create some testdata execute  
   ```docker exec -it <inyoka_workercontainer> /inyoka/venv/bin/python ./make_testdata.py```
 * To create a superuser account named `admin` execute  
   ```docker exec -it <inyoka_workercontainer> /inyoka/venv/bin/python manage.py create_superuser --username admin --email 'admin@localhost'```


Development: E-Mail logs
------------------------

(only for _development_ setups)

E-Mail logs can be viewed via `docker service logs -f inyoka-dev_inyoka-worker`


Development: TLS certificates
-----------------------------

(only for _development_ setups)

For the development setup, caddy automatically creates self-signed TLS certificates.

To get the local TLS root certificate of caddy execute

```
docker exec -it <caddy container id> cat /data/caddy/pki/authorities/local/root.crt > caddy_local_root.crt
```

It is recommended to use a separate browser profile only for local development. In this separate profile you can import the root certificate.
The local root CA will not change as long as the caddy volumes are the same.

As an alternative, you can also trust all `*.ubuntuusers.localhost` domains manually.
However, the leaf certificates seem to be only valid for one day.

View service logs
-----------------

```
docker service logs <service name from service ls>
```

 * Add `-f` to follow for new entries

Remove the stack
----------------

 - for _development_  
```
docker stack rm inyoka-dev
```

 - for _production_  
```
docker stack rm inyoka
```


Other notes
-----------

 * "Where is Docker storing my data when I use a named volume?"  
   `docker volume inspect <volume-name>`
 * View the merged development stack config  
   `docker stack config -c docker-compose.yaml -c docker-development.yml |& less`
 * Compare production and development stack config    
   `vimdiff <(docker stack config -c docker-compose.yaml) <(docker stack config -c docker-compose.yaml -c docker-development.yml)`
 * How to check, if clamav works and what it does  
   `clamdtop "/etc/clamav/sockets/clamd.sock"` or `clamdtop clamav`

Components used
----------------

A list of links to the release page of used components (and their RSS-feeds).

 * [Supported Debian releases](https://wiki.debian.org/DebianReleases#Production_Releases)
 * [Alpine releases](https://alpinelinux.org/releases/)
 * [Caddy releases](https://github.com/caddyserver/caddy/releases) ([Feed](https://github.com/caddyserver/caddy/releases.atom))
 * [Clamav releases](https://www.clamav.net/downloads) ([Feed](https://github.com/Cisco-Talos/clamav/releases.atom))
 * [Python releases](https://www.python.org/downloads/) ([Feed](https://github.com/python/cpython/releases.atom))
 * [Redis releases](https://github.com/redis/redis/releases) ([Feed](https://github.com/redis/redis/releases.atom))
 * [Supported postgreSQL releases](https://www.postgresql.org/support/versioning/) ([Feed](https://www.postgresql.org/news/pgsql.rss))
