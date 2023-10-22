# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Update package lists
RUN apt-get update

# Install ping utility
RUN apt-get install -y iputils-ping

# Copy the rest of the files
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 8082

# Run your Flask app
CMD ["python", "-u" ,"app.py"]
