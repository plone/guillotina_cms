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


Running Plone-React
-------------------

Checkout Plone-React::

    git clone https://github.com/plone/plone-react.git
 
Install JS package dependencies with Yarn::

    cd plone-react
    yarn install

Then edit "src/config/index.js" to point to http://localhost:8081/db/web.

Start frontend dev server::

    yarn dev

Then go to http://localhost:4300 to see the Plone-React frontend running on Guillotina!

You can log into Plone-React with username "root" and password "root".


Cleanup DB
----------

Cleanup postgres env::

    docker-compose -f docker-compose-pg.yaml rm -s -v elasticsearch redis postgres

Cleanup cockroachdb env::

    docker-compose -f docker-compose-pg.yaml rm -s -v elasticsearch redis cockroachdb cockroachdb2


Optional addons
---------------

- guillotina_linkintegrity
