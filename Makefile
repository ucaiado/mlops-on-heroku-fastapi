SHELL := /bin/bash
DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

docker-build:  ## Build the Docker image used in this project
	cp ~/.netrc .;
	docker build . --progress tty -t udacity/mlops_tests_2:latest ;
	rm .netrc

linter:  ## Lint library files
	docker-compose \
	-p mlops \
	-f docker-compose.yml \
	run --rm -w /opt mlops \
	bash scripts/linter-code.sh steps/src/train_random_forest/*.py

bash:  ## Open an interactive terminal in Docker container
	docker-compose \
	-p mlops \
	-f docker-compose.yml \
	run --rm mlops