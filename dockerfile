# Use a lightweight Python image
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Set environment variables for Chrome
ENV PATH="/usr/bin/chromium:${PATH}"
ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROME_DRIVER="/usr/bin/chromedriver"

# Command to run your application using Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]