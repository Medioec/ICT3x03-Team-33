# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt
COPY sessioncleaning/requirements.txt /app

# Update package lists
RUN apt-get update

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy app directory contents into the container at /app
COPY databaseservice/ /app

# Run your Flask app
CMD ["python", "./app.py"]