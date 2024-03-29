JSON_FILES 			= $(wildcard configurations/*.json)
JSON_FILE_NOTDIR 	= $(notdir $(wildcard configurations/*.json))
ENV_FILE			= docker/.env
IMAGE				= message_on_live:twitch
DOCKER_COMPOSE_FILE	= docker/docker-compose.yml
APP_ID				= qn9dgxv87jm94tkdufaruuhq52nqz3

############################################################################

all: stop init-env build run

stop:
	@if [ -n "$$(docker ps --filter ancestor=$(IMAGE) | grep $(IMAGE))" ]; then \
		docker stop $$(docker ps --filter ancestor=$(IMAGE) -q); \
		echo "\033[0;32m[✔️] All containers have been stopped\033[0m"; \
	fi

build:
	@mkdir -p logs/
	@docker pull python:alpine3.19
	@echo           "#####################################################################################################"
	@echo "\033[0;33mIN CASE OF DOCKER PERMISSION DENIED, USE: make sudo or make sudo-stop, make sudo-build, make sudo-run\033[0m"
	@echo           "#####################################################################################################"
	@docker-compose -f $(DOCKER_COMPOSE_FILE) build
	@echo "\033[0;32m[✔️] docker-compose built successfully\033[0m"

run: $(mkdir-logs) $(check-characters) $(JSON_FILES:.json=.up)

%.up: %.json
	@echo "Launching docker-compose up with $(notdir $<)"
	$(shell export JSON_FILE=$(notdir $<) JSON_FILE_TRUNC=$$(echo $(notdir $<) | sed 's/\.json//g') && docker-compose -p mol_$$(echo $(notdir $<) | sed 's/\.json//g') -f $(DOCKER_COMPOSE_FILE) up -d)

############################################################################

init-env:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "\033[0;32mPreparing to create $(ENV_FILE) file...\033[0m"; \
		printf "Get an oauth token at : \e[4m%s\e[0m\n" "https://titouanck.github.io/Twitch-messageOnLive/" && \
		read -p "Enter USER_TOKEN: " user_token && \
		echo "Creating $(ENV_FILE) file..." && \
		echo "APP_ID=$(APP_ID)" > $(ENV_FILE) && \
		echo "USER_TOKEN=$$user_token" >> $(ENV_FILE); \
	else \
		echo "\033[0;32m$(ENV_FILE) already exists.\033[0m"; \
	fi

check-characters:
	@if find configurations -name '*.json' -exec basename {} .json \; | cat | grep -q '[^[:alnum:]_-]'; then \
        echo "\033[0;31m[X] At least one invalid .json filename, use only [a-z, A-Z, 0-9, _, -]\033[0m"; \
		exit 1; \
	fi

mkdir-logs:
	@mkdir -p logs/


############################################################################

sudo: mkdir-logs
	sudo make all

sudo-stop: mkdir-logs
	sudo make stop

sudo-build: mkdir-logs
	sudo make build

sudo-run: mkdir-logs
	sudo make run

############################################################################

clean:
	rm -rf logs/ docker/app/__pycache__/

fclean: $(clean)
	rm -f docker/.env

.PHONY: all stop build run init-env check-characters mkdir-logs clean fclean

############################################################################
