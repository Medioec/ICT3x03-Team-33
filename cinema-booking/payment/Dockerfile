# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Update package lists
RUN apt-get update

# Install ping utility
RUN apt-get install -y iputils-ping

# Copy the current directory contents into the container at /app
COPY payment/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy common files
COPY common/ /app

# Copy app directory contents into the container at /app
COPY payment/ /app

# Make port 80 available to the world outside this container
EXPOSE 8084

# Run your Flask app
CMD ["python", "app.py"]
