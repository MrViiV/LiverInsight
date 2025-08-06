# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Install Node and npm
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && npm install

# Expose ports (choose your backend port, e.g., 8000)
EXPOSE 8001

# Start your backend and frontend services
CMD ["sh", "-c", "python3 install_ml_dependencies.py && ./start_services.sh"]
