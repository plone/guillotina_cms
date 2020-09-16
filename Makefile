# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Builds the environment
	virtualenv --clear --python=python3 .
	bin/pip install --upgrade pip
	bin/pip install -r requirements.txt
	bin/python setup.py develop
	docker-compose create
	docker-compose -f docker-compose.yaml up postgres
	make populate

initdb: ## Create initial content in the DB
	bin/initdb

deletedb: ## Deletes and resets the DB
	bin/deletedb

start-backend: ## Starts Guillotina
	guillotina -c config-pg.yaml

start-dependencies: ## Starts dependencies (PG, ES, Redis)
	docker-compose -f docker-compose.yaml up postgres

docker:
	docker build -t plone/guillotina_cms:latest .
	docker push plone/guillotina_cms:latest
