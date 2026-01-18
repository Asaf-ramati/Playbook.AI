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

# Make start script executable
RUN chmod +x start.sh

# Expose port (Railway will use PORT env var)
EXPOSE 8000

# Start LangGraph dev server
CMD ["./start.sh"]