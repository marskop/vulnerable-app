# Use a lightweight Python image
FROM python:3.8-slim

# Upgrade pip and install necessary packages
RUN pip install --upgrade pip
RUN pip install bandit semgrep trufflehog

# Set the working directory to /app inside the container
WORKDIR /app

# Copy only the contents of the app/ directory to /app in the container
COPY ./app /app

# Default command to run when the container starts
CMD ["/bin/bash"]
