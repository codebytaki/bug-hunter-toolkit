# Bug Hunter Toolkit - Docker Image
FROM python:3.11-slim

LABEL maintainer="Taki <codebytaki@github.com>"
LABEL description="Professional Security Testing Toolkit"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nmap \
    git \
    curl \
    wget \
    dnsutils \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY bug_hunter.py .
COPY wordlists/ ./wordlists/

# Create logs directory
RUN mkdir -p logs

# Make CLI executable
RUN chmod +x bug_hunter.py

# Set Python path
ENV PYTHONPATH=/app

# Default command
ENTRYPOINT ["python", "bug_hunter.py"]
CMD ["--help"]
