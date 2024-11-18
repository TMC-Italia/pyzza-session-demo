# Makefile

# Install the required packages
install:
	@echo "Installing requirements..."
	pip install -r dev-requirements.txt

compose-build:
	docker compose build

# Run the program, in auto reload mode
compose-up:
	docker compose up -d --remove-orphans

# Run the Ollama with Gemma2:2b in terminal
run-in-terminal:
	docker exec -it ollama_service ollama run gemma2:2b

compose-down:
	docker compose down --remove-orphans

compose-destroy:
	docker compose down -v --remove-orphans

compose-restart:
	docker compose restart

compose-logs:
	docker compose logs -f

rebuild: compose-down compose-build compose-up compose-logs