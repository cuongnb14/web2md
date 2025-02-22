# Use an official Python runtime as a parent image
FROM python:3.11-slim

ENV REFRESHED_AT=2025-02-22

RUN apt-get update -qq

# Libs for run Playwright Browser
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libglib2.0-0 libnss3 \
    libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxcb1 libxkbcommon0 libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 \
    libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2

# Install Playwright
RUN pip install playwright==1.50.0
RUN playwright install chromium

ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install required Python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the default command to run the crawler
CMD ["python", "main.py"]
