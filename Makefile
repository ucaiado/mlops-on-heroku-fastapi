SHELL := /bin/bash
DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

docker-build:  ## Build the Docker image used in this project
	cp ~/.netrc .;
	docker build . --progress tty -t udacity/mlops_tests_2:latest ;
	rm .netrc

bash:  ## Open an interactive terminal in Docker container
	docker-compose \
	-p mlops \
	-f docker-compose.yml \
	run --rm mlops

lint-with-pylint:  ## Lint library files
	docker-compose \
	-p mlops \
	-f docker-compose.yml \
	run --rm -w /opt mlops \
	bash /root/project/scripts/linter-code.sh /root/project/starter/starter/ml/*.py

create-iam:  ## Create an IAM user with the appropriate permissions
	python scripts/iac.py -i

create-bucket:  ## Create a new bucket in S3 with name specified in scripts/confs/project.cfg
	python scripts/iac.py -b

setup-dvc:  ## Setup DVC to use the bucket specified in the conf file
	dvc init -f;
	python scripts/iac.py -d

setup-aws-to-github:  ## Setup AWS credentials to github
	python scripts/iac.py -g

dvc-push-data:  ## Push data to dvc remote
	docker-compose \
	-p dvc-push-data \
	-f docker-compose.yml \
	run --rm dvc-push-data

clean-data:  ## Clean data and include in DVC
	docker-compose \
	-p clean-data \
	-f docker-compose.yml \
	run --rm clean-data

training-model:  ## Training the model on cleaned data
	docker-compose \
	-p training-model \
	-f docker-compose.yml \
	run --rm training-model

lint-and-test:  ## Lint library files, repeting tests performed by Github Actions
	docker-compose \
	-p lint-and-test \
	-f docker-compose.yml \
	run --rm lint-and-test

local-api:  ## Launch API locally
	docker-compose \
	-p local-api \
	-f docker-compose.yml \
	run --service-ports --rm local-api

sanity-check:  ## Run sanitycheck script
	docker-compose \
	-p sanity-check \
	-f docker-compose.yml \
	run --service-ports --rm sanity-check

create-heroku-app:  ## Create a heroku app
# 	heroku create > heroku_output.txt;
	python scripts/iac.py -hr;
	@echo "!! look at heroku_output.txt file"

deploy-heroku-app:  ## Deploy the heroku app
	git push heroku main

get-logs-heroku:  ## Get logs from Heroku application
	heroku logs --tail
