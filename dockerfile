# Base image
FROM python:3.9-slim

# Copy application code
WORKDIR /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Initialize the database
RUN python init_db.py

# Run the application
CMD ["python", "app.py"]
