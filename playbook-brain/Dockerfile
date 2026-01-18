FROM python:3.11-slim
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y curl gcc && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app

# Expose port (Railway will use PORT env var)
EXPOSE 8000

# Start LangGraph dev server
CMD ["python", "-m", "langgraph_cli", "dev", "--port", "8000", "--host", "0.0.0.0"]