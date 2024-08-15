# Base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Initialize the database (only if init_db.py is present and necessary)
# RUN python init_db.py

# Run the application
CMD ["python", "app.py"]
