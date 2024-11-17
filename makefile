# Makefile

# Install the required packages
install:
	@echo "Installing requirements..."
	pip install -r dev-requirements.txt

compose-build:
	docker compose build

# Run the program, in auto reload mode
compose-up:
	docker compose up -d

compose-down:
	docker compose down --remove-orphans

compose-destroy:
	docker compose down -v --remove-orphans

compose-restart:
	docker compose restart

compose-logs:
	docker compose logs -f