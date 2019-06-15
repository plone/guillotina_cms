.. contents::

GUILLOTINA_CMS
==============

WIP: This package is a work in progress to provide CMS on guillotina

Bundle of cms functionality for guillotina


Prepare Docker env
------------------

MacOS::

    screen ~/Library/Containers/com.docker.docker/Data/vms/0/tty
    sysctl -w vm.max_map_count=262144
    (to exit Ctrl + a + d)

Quick Start
-----------

There's in place a convenience Makefile that setups all the basic enviroment
required for Guillotina CMS to work::

    make

It will install the default virtualenv, pull and launch the docker containers,
and setup the default objects in the DB for the CMS to work. If you do this,
you can pass on the next steps. Follow the next steps in case you want to have
more control over how the environment is set up.

You can always run::

    make initdb

to populate the DB. You can run::

    make deletedb

to reset and remove the default container.

Start Docker Background
-----------------------

Start it (with cockroach) ::

    docker-compose create
    docker-compose up cockroachdb cockroachdb2 elasticsearch redis
    docker exec -it guillotina_cms_cockroachdb_1 /cockroach/cockroach sql --insecure --execute="CREATE DATABASE guillotina;"


Start it (with postgres) ::

    docker-compose create
    docker-compose -f docker-compose-pg.yaml up postgres elasticsearch redis

Build dev image (a.k.a. ./bin/buildout)
---------------------------------------

To install with docker::

    docker-compose build guillotina

To install with virtualenv (python 3.7) ::

    virtualenv .
    source bin/activate
    pip install -r requirements.txt
    python setup.py develop
    # If you want to run tests
    pip install -r requirements-test.txt


Run dev (a.k.a. ./bin/instance fg)
----------------------------------

Run docker dev container (with cockroach) ::

    docker-compose run --service-ports guillotina

Run docker dev container (with postgres) ::

    docker-compose -f docker-compose-pg.yaml run --service-ports guillotina

Run on virtualenv (with postgres) ::

    g -c config-pg.yaml


Add CMS container
-----------------

Add CMS containers::

    curl -X POST --user root:root http://localhost:8081/db -d '{"@type": "Container", "id": "web", "title": "Plone Site"}'
    curl -X POST --user root:root http://localhost:8081/db/web/@addons -d '{"id": "cms"}'


Using Executioner (optional)
----------------------------

If you want to access and browse the guillotina tree you can use the Angular Front::

    http://localhost:8081/+admin


Running Volto
-------------------

Checkout Volto::

    git clone https://github.com/plone/volto.git

Install JS package dependencies with Yarn::

    $ cd volto
    $ yarn

Then edit "src/config/index.js" to change the default Plone backend parameter
``RAZZLE_API_PATH``::

    apiPath: process.env.RAZZLE_API_PATH || 'http://localhost:8081/db/web

then start the server in development mode::

    $ yarn start

or alternativelly, setup the environment variable to modify it::

    $ RAZZLE_API_PATH=http://localhost:8081/db/web yarn start

Then go to http://localhost:3000 to see the Volto frontend running on Guillotina!

You can log into Volto with username "root" and password "root".

If you are interested in start a Volto project instead of developing Volto, you
can follow the instructions in::

    https://docs.voltocms.com/01-getting-started/01-install/#install-volto

Cleanup DB
----------

Cleanup postgres env::

    docker-compose -f docker-compose-pg.yaml rm -s -v elasticsearch redis postgres

Cleanup cockroachdb env::

    docker-compose -f docker-compose-pg.yaml rm -s -v elasticsearch redis cockroachdb cockroachdb2


Optional addons
---------------

- guillotina_linkintegrity
