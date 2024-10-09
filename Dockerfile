# Use an official Python 3.12 slim image as a base
FROM python:3.12-slim

# Set environment variables to ensure non-interactive installs
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install any necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools wheel

# Install the CS50 package (includes check50, submit50, etc.)
RUN pip install cs50

# Set the working directory inside the container
WORKDIR /workspaces/CS50AI 

# Copy the current directory contents into the container
COPY . .

# Expose a port if needed (e.g., if running a web app)
# EXPOSE 8080

# Define the default command to run your app or use a specific entry point for the course
CMD ["bash"]
