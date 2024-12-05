
# Pyzza Session Demo 🍕  
**Python Demo - Pizza Session (18 Nov)**  

This repository demonstrates a Python-based application designed for a pizza-themed session, showcasing various services built with Docker, Python, and Makefiles.  

## Project Overview  

This project consists of a modular setup, with multiple services that serve as independent microservices. These services include:  

- **API**: Provides core API functionalities.
- **HR Assistant**: A service to assist with HR-related tasks.
- **PDF Generator**: A tool for generating PDFs based on user inputs.
- **Song Generator**: A service for generating songs using AI.
- **Telegram Bot**: A bot integrated with Telegram to perform various operations.

Each service has its own `Dockerfile`, `main.py`, and `requirements.txt` for isolation and scalability.  

## Installation  

### Python Environment Setup:  

1. Create and activate a virtual environment:  

   ```bash
   python3 -m venv .venv
   . .venv/bin/activate
   ```  

   To confirm the virtual environment is activated, run:  

   ```bash
   which python
   ```  

2. Copy the sample environment variables file and customize it:  

   ```bash
   cp .env.sample .env
   ```  

   Edit the `.env` file to set your custom environment variables.  

### Install the Dependencies:  

   ```bash
   make install
   ```  

## Usage  


### Building and Running the Containers  

1. Build the containers:  

   ```bash
   make compose-build
   ```  

2. Run the containers:  

   ```bash
   make compose-up
   ```  

3. View logs:  

   ```bash
   make compose-logs
   ```  

4. Stop and clean up the containers:  

   ```bash
   make compose-down
   ```  

5. Destroy the containers and volumes:  

   ```bash
   make compose-destroy
   ```  

6. Restart the containers:  

   ```bash
   make compose-restart
   ``` 

## Run gemma2:2b  

Run the Ollama with Gemma2:2b in terminal.

```bash
make run-in-terminal
``` 

## Makefile Explanation  

This repository uses a Makefile to simplify development workflows:  

- `install`: Installs the required dependencies from `dev-requirements.txt`.  
- `compose-build`: Builds the Docker containers.  
- `compose-up`: Starts the containers in detached mode, removing orphan containers.  
- `compose-down`: Stops and removes the containers.  
- `compose-destroy`: Stops the containers and removes associated volumes.  
- `compose-restart`: Restarts the running containers.  
- `compose-logs`: Displays live logs from the running containers.  
- `rebuild`: Combines `compose-down`, `compose-build`, and `compose-up` steps for rebuilding the containers from scratch.  
- `run-in-terminal`: Runs the Ollama service with Gemma2:2b interactively.  

## Directory Structure  

```plaintext
.github/workflows/
    docker-publish.yml       # GitHub Actions workflow for Docker publishing

api/
    Dockerfile               # Dockerfile for the API service
    main.py                  # Main entry point for the API
    requirements.txt         # Dependencies for the API

services/
    hr_assistant/
    pdf_generator/
    song_generator/
    telegram_bot/

.env.sample                  # Sample environment variables file
.gitignore                   # Git ignore rules
dev-requirements.txt         # Development dependencies
docker-compose.yml           # Docker Compose configuration
docker-compose-prod.yml      # Production Docker Compose configuration
Makefile                     # Simplified commands for project management
README.md                    # Project documentation
```  

## License  

This project is distributed under the MIT License.  

## Contributing  

Feel free to fork this repository and submit pull requests to improve the project!  
