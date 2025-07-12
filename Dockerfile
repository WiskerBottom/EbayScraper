# Use the official Ubuntu image as a base
FROM fedora:latest

# Install the required dependencies
RUN dnf -y update && dnf install -y python3 python3-pip chromium-browser && dnf clean all
RUN pip3 install selenium

# Set the working directory to /app
WORKDIR /app

# Copy the project code into the container
COPY . /app/

#RUN mkdir -p /app/Details

#RUN useradd -m florence  # Creates a new user "florence" with a home directory
#USER florence  # Sets the user for subsequent commands

# Expose the port where the Selenium server will run
EXPOSE 8000
