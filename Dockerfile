FROM python:3.11-slim

# 1. Install system dependencies and Chrome securely
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    --no-install-recommends \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Setup Webdriver Manager Cache
RUN mkdir -p /root/.wdm && chown -R root:root /root/.wdm

# 3. Setup Python Environment
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy test files
COPY tests/ ./tests/
RUN mkdir -p /app/test-results
