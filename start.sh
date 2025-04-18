#!/bin/bash

# Start script for Code Review Assistant
# This script starts both the API server and MCP server

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if dependencies are installed
check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
        exit 1
    fi
    
    # Check pip
    if ! command -v pip &> /dev/null; then
        echo -e "${RED}pip is not installed. Please install pip.${NC}"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}Node.js is not installed. Please install Node.js 16 or higher.${NC}"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}npm is not installed. Please install npm.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}All dependencies are installed.${NC}"
}

# Function to install dependencies
install_dependencies() {
    echo -e "${BLUE}Installing backend dependencies...${NC}"
    cd backend && pip install -r requirements.txt
    
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    cd ../frontend && npm install
    
    echo -e "${GREEN}All dependencies installed successfully.${NC}"
}

# Function to check environment files
check_env_files() {
    if [ ! -f backend/.env ]; then
        echo -e "${YELLOW}Warning: .env file not found in backend directory. Creating from example...${NC}"
        cp backend/.env.example backend/.env
        echo -e "${YELLOW}Please update backend/.env with your GitHub token and other settings.${NC}"
    fi
}

# Function to start the API server
start_api_server() {
    echo -e "${BLUE}Starting API server on port 8000...${NC}"
    cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
    API_PID=$!
    echo -e "${GREEN}API server started with PID ${API_PID}${NC}"
}

# Function to start the MCP server
start_mcp_server() {
    echo -e "${BLUE}Starting MCP server on port 8080...${NC}"
    cd backend && python -m uvicorn mcp_server:mcp_app --host 0.0.0.0 --port 8080 &
    MCP_PID=$!
    echo -e "${GREEN}MCP server started with PID ${MCP_PID}${NC}"
}

# Function to start the frontend
start_frontend() {
    echo -e "${BLUE}Starting frontend on port 3000...${NC}"
    cd frontend && npm run dev &
    FRONTEND_PID=$!
    echo -e "${GREEN}Frontend started with PID ${FRONTEND_PID}${NC}"
}

# Handle Ctrl+C
trap ctrl_c INT
function ctrl_c() {
    echo -e "${YELLOW}Stopping all services...${NC}"
    kill $API_PID $MCP_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Main script
echo -e "${BLUE}=== Code Review Assistant Startup ===${NC}"

# Check and install dependencies
check_dependencies
check_env_files

# Check if --install flag is provided
if [ "$1" == "--install" ]; then
    install_dependencies
fi

# Start services
start_api_server
start_mcp_server
start_frontend

# Display URLs
echo -e "${GREEN}=== Services Started ===${NC}"
echo -e "${GREEN}API Server:${NC} http://localhost:8000"
echo -e "${GREEN}MCP Server:${NC} http://localhost:8080"
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"

# Wait for user to press Ctrl+C
wait
