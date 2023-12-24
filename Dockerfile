FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .

# Command to run on container start
ENTRYPOINT ["python", "./app.py"]
