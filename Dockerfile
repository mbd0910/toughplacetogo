# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Install dockerize
RUN apt-get update && apt-get install -y wget
RUN wget -qO- https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz | tar xvz -C /usr/local/bin

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt first, for caching the layer
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# For saving files
RUN mkdir -p /data

# Copy the rest of the application
COPY . .

# Command to run the application
#CMD ["dockerize", "-wait", "tcp://db:5432", "-timeout", "60s", "python", "app/fpl_import.py"]

# Command to keep the container running
CMD ["tail", "-f", "/dev/null"]
