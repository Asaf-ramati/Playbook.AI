#!/bin/bash

# Use Railway's PORT if available, otherwise default to 8000
PORT=${PORT:-8000}

echo "Starting LangGraph server on port $PORT..."

# Start LangGraph dev server
langgraph dev --port $PORT --host 0.0.0.0