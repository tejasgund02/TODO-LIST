# Use an official Nginx image as the base image
FROM nginx:latest

# Set the working directory
WORKDIR /usr/share/nginx/html

# Remove default Nginx static files
RUN rm -rf ./*

# Copy the frontend files into the container
COPY . .

# Expose port 80 for the frontend
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
