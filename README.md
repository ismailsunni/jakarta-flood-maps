# Welcome to the Jakarta Flood Mapper code base!

Jakarta Flood Mapper is a django application for mapping floods in Jakarta.
With a bit of tweaking the application could probably be used for other
localities in Indonesia fairly easily, and with a little more it could
be used in other parts of the world.

**Please note that this project is in the early phase of its development.**

You can visit a running instance of this project at
[http://jfm.kartoza.com](http://jfm.kartoza.com).

# Status

These badges reflect the current status of our development branch:

Tests status: [![Build Status](https://travis-ci.org/kartoza/jakarta-flood-maps-django.svg)](https://travis-ci.org/kartoza/jakarta-flood-maps-django)

Coverage status: [![Coverage Status](https://coveralls.io/repos/kartoza/jakarta-flood-maps/badge.png?branch=develop)](https://coveralls.io/r/kartoza/jakarta-flood-maps?branch=develop)

Development status: [![Stories in Ready](https://badge.waffle.io/kartoza/jakarta-flood-maps.svg?label=ready&title=Ready)](http://waffle.io/kartoza/jakarta-flood-maps) [![Stories in Ready](https://badge.waffle.io/kartoza/jakarta-flood-maps.svg?label=In%20Progress&title=In%20Progress)](http://waffle.io/kartoza/jakarta-flood-maps)

# License

Code: [Free BSD License](http://www.freebsd.org/copyright/freebsd-license.html)

Out intention is to foster wide spread usage of the data and the code that we
provide. Please use this code and data in the interests of humanity and not for
nefarious purposes.

# Setup instructions

## Simple deployment under docker

### Overview

You need two docker containers:

* A postgis container
* A uwsgi container

We assume you are running nginx on the host and we will set up a reverse
proxy to pass django requests into the uwsgi container. Static files will
be served directly using nginx on the host.

A convenience script is provided under ``scripts\create_docker_env.sh`` which
should get everything set up for you. Note you need at least docker 1.2 - use
the [installation notes](http://docs.docker.com/installation/ubuntulinux/)
on the official docker page to get it set up.

### Check out the source


First checkout out the source tree:

```
git clone git://github.com/kartoza/jakarta-flood-maps.git
```

### Build your docker images and run them

You need to have http://docker.io and http://www.fig.sh/ installed first.

Note you need at least docker 1.2 - use
the [installation notes](http://docs.docker.com/installation/ubuntulinux/)
on the official docker page to get it set up.

Fig will build and deploy the docker images for you. Note if you are using
``apt-cacher-ng`` (we recommend it as it will dramatically speed up build
times), be sure to edit ``docker-prod/71-apt-cacher-ng`` and comment out
existing lines, adding your own server. Alternatively if you wish to fetch
packages are downloaded directly from the internet, ensure that all lines are
commented out in your hosts:

* ``docker-prod/71-apt-cacher-ng``
* ``docker-dev/71-apt-cacher-ng``


```
cd deployment
fig build
fig up -d uwsgi
fig run migrate
fig run collectstatic
```

### Setup nginx reverse proxy

You should create a new nginx virtual host - please see
``jakarta-flood-maps-nginx.conf`` in the root directory of the source for an example.


## For local development

### Install dependencies

```
virtualenv venv
source venv/bin/activate
pip install -r REQUIREMENTS-dev.txt
nodeenv -p --node=0.10.31
npm -g install yuglify
```

### Create your dev profile


```
cd django_project/core/settings
cp dev_timlinux.py dev_${USER}.py
```

Now edit ``dev_<your username>`` setting your database connection details as
needed. We assume you have created a postgres (with postgis extentions)
database somewhere that you can use for your development work. See
[http://postgis.net/install/](http://postgis.net/install/) for details on doing
that.

### Running migrate, collect static, and development server

Prepare your database and static resources by doing this:

```
virtualenv venv
source venv/bin/activate
cd django_project
python manage.py migrate --settings=core.settings.dev_${USER}
python manage.py collectstatic --noinput --settings=core.settings.dev_${USER}
python manage.py runserver --settings=core.settings.dev_${USER}
```

**Note:** You can also develop in docker using the instructions provided in
[README-dev.md](https://github.com/kartoza/jakarta-flood-maps/blob/develop/README-dev.md).




