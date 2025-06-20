# Base image
FROM python:3.12-slim-bookworm

# Avoid prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install Chromium and system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    xvfb \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable for headless display
ENV DISPLAY=:99

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Copy your backend application code
COPY server .

# Optional: Expose API port (if using Flask, FastAPI, etc.)
EXPOSE 8000

# Run the application (adjust if using something like uvicorn for FastAPI)
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
