# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy the code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask redis pillow

# Expose the port
EXPOSE 8000

# Run the script
CMD ["python", "Server.py","run", "--host=0.0.0.0"]
