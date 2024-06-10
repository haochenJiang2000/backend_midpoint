# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements_mid.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application with gunicorn
CMD ["gunicorn", "-w", "6", "--bind", "0.0.0.0:5000", "--timeout", "300", "app:app"]
