# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt
COPY identity/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Update package lists
RUN apt-get update

# Install ping utility
RUN apt-get install -y iputils-ping

# Install wget
RUN apt-get install -y wget

# Create a directory for the wordlist
RUN mkdir /app/wordlist

# Download the blacklistedPW
RUN wget -O /app/wordlist/blacklistedPW.txt https://raw.githubusercontent.com/danielmiessler/SecLists/aad07ff/Passwords/10_million_password_list_top_100000.txt

# Copy common files
COPY common/ /app

# Copy app directory contents into the container at /app
COPY identity/ /app

# Make port 443 available to the world outside this container
EXPOSE 443

# Run your Flask app
CMD gunicorn --preload --certfile=fullchain.pem --keyfile=privkey.pem --conf gunicorn_conf.py --bind 0.0.0.0:443 wsgi:app
