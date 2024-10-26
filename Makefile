# Define paths
VENV = venv
REQS = requirements.txt
BE = be
FE = fe

# Default goal
.DEFAULT_GOAL := help

# Help command
help:
	@echo "Available commands:"
	@echo "  make venv        - Create a Python virtual environment and install dependencies"
	@echo "  make backend     - Run the backend (Python) application"
	@echo "  make frontend    - Install dependencies and start the React frontend"
	@echo "  make clean       - Remove all generated files and directories"
	@echo "  make install_all - Install dependencies for both backend and frontend"
	@echo "  make lint        - Run code linting for both backend and frontend"
	@echo "  make format      - Format code for both backend and frontend"

# Set up Python virtual environment and install requirements
venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r $(REQS)
	@echo "Virtual environment created and dependencies installed."

# Run backend
backend:
	$(VENV)/bin/uvicorn be.main:app --reload

# Set up frontend
frontend:
	cd $(FE) && npm install && npm start

# Install all dependencies
install_all: venv frontend

# Clean up
clean:
	rm -rf $(VENV)
	rm -rf $(FE)/node_modules
	rm -rf __pycache__
	rm -rf $(BE)/__pycache__
	@echo "Cleaned up generated files."

# Lint both frontend and backend
lint:
	$(VENV)/bin/flake8 $(BE)
	cd $(FE) && npm run lint

# Format code for both frontend and backend
format:
	$(VENV)/bin/isort $(BE)
	$(VENV)/bin/black $(BE)
	cd $(FE) && npx prettier --write .

lint-flake8:
	@echo "Running flake8 to check for style issues..."
	$(VENV)/bin/flake8 $(BE) || (echo "Flake8 failed. Please fix the issues before continuing." && exit 1)