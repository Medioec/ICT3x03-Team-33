# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY booking/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Update package lists
RUN apt-get update

# Install ping utility
RUN apt-get install -y iputils-ping

# Copy common files
COPY common/ /app

# Copy app directory contents into the container at /app
COPY booking/ /app

# Make port 443 available to the world outside this container
EXPOSE 443

# Run your Flask app
CMD gunicorn --conf gunicorn_conf.py wsgi:app
