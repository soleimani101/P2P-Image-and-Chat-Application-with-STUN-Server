# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app/Peer

# Copy the code into the container
COPY . /app/Peer

# Install dependencies
RUN pip install --no-cache-dir requests pillow tqdm

# Expose the port
EXPOSE 8000

# Run the script
CMD ["python", "Peer.py"]
