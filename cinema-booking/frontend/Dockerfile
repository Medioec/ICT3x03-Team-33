# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory to /app/frontend
WORKDIR /app

# Copy package.json
COPY package.json .

# Install any necessary dependencies
RUN npm install

# Copy the contents of the local frontend directory into the container
COPY . .

EXPOSE 8080

# Start your application
CMD ["npm", "start"]
