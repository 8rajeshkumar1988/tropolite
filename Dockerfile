# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /docker_app

# Install dependencies
COPY requirements.txt /docker_app/
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /docker_app/
