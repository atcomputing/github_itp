FROM docker.io/python:3.11.14-trixie

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY files/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and tests
COPY files/app .

# Create directory for image storage
RUN mkdir -p /pictures

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variables
ENV FLASK_ENV=production
ENV PICTURES_DIR=/pictures

# Run app.py when the container launches
CMD ["python3.11", "-m" , "flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port", "5001"]
