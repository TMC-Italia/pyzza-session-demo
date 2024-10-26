# Makefile

# Install the required packages
install-dependencies:
	@echo "Installing required packages..."
	@pip install -r requirements.txt

compose-build:
	docker compose build

# Run the program, in auto reload mode
compose-up:
	docker compose pull
	docker compose up -d

compose-down:
	docker compose down

compose-restart:
	docker compose restart

compose-destroy:
	docker compose down

compose-logs:
	docker compose logs -f