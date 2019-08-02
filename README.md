Run inyoka and themes in docker
============================

requirements
-------------

 * [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu)
 * [docker-compose](https://github.com/docker/compose/releases)

prepare
-------

prepare working directory (take note of the '.' in the second line)
```
cd /srv/www
git clone git@github.com:inyokaproject/docker-setup.git .
git clone git@github.com:inyokaproject/inyoka.git
git clone git@github.com:inyokaproject/theme-ubuntuusers.git
```

prepare inyoka config:

```cd /srv/www && cp development_settings.py inyoka/```

build docker image:

```cd /srv/www && docker-compose build```

run in foreground

```cd /srv/www && docker-compose up```

run in background

```cd /srv/www && docker-compose up -d```

show logs from running in background

```cd /srv/www && docker-compose logs```

stop running in background

```cd /srv/www && docker-compose down```


