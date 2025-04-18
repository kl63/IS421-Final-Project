.PHONY: setup-backend setup-frontend install-all test-backend test-frontend test-all run-backend run-frontend run-all docker-build docker-up docker-down clean

# Setup commands
setup-backend:
	cd backend && pip install -r requirements.txt

setup-frontend:
	cd frontend && npm install

install-all: setup-backend setup-frontend

# Test commands
test-backend:
	cd backend && python -m unittest discover -s tests

test-frontend:
	cd frontend && npm test

test-all: test-backend test-frontend

# Run commands
run-backend:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-mcp:
	cd backend && uvicorn mcp_server:mcp_app --reload --host 0.0.0.0 --port 8080

run-frontend:
	cd frontend && npm run dev

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# Clean command
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name ".next" -exec rm -rf {} +

# Help command
help:
	@echo "Available commands:"
	@echo "  setup-backend     - Install backend dependencies"
	@echo "  setup-frontend    - Install frontend dependencies"
	@echo "  install-all       - Install all dependencies"
	@echo "  test-backend      - Run backend tests"
	@echo "  test-frontend     - Run frontend tests"
	@echo "  test-all          - Run all tests"
	@echo "  run-backend       - Run backend server"
	@echo "  run-mcp           - Run MCP server"
	@echo "  run-frontend      - Run frontend development server"
	@echo "  docker-build      - Build Docker containers"
	@echo "  docker-up         - Start Docker containers"
	@echo "  docker-down       - Stop Docker containers"
	@echo "  clean             - Clean build artifacts"
