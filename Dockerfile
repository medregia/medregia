# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /medregia

# Install MySQL client and other necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       pkg-config \
       default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
COPY requirements.txt /medregia/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /medregia
COPY . /medregia

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
