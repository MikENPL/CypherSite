.PHONY: build dev run stop

build:
	docker compose build

dev: 
	docker compose -f compose.yaml -f compose.dev.yaml up

run: 
	docker compose up

stop:
	docker compose down
