.PHONY: build dev run stop
.DEFAULT_GOAL := help
build:
	@docker compose build

dev: 
	@docker compose -f compose.yaml -f compose.dev.yaml up 

run: 
	@docker compose up 

stop:
	@docker compose down
help:
	@echo "CypherSite - Available commands"
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  help   Display this help message"
	@echo "  build  Build the Docker image"
	@echo "  dev    Start the development environment"
	@echo "  run    Start the application"
	@echo "  stop   Stop running containers"
