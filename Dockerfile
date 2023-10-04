# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim-bullseye

# Expose port 5000 for the Flask application to run on.
EXPOSE 5000/tcp

# Set the working directory in the Docker image filesystem.
WORKDIR /blog

# Copy the dependencies file to the working directory.
COPY requirements.txt .

# Upgrade pip to ensure the latest version is used.
# Then, install any dependencies.
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the content of the local src directory to the working directory.
COPY . .

# Add a non-root user and switch to it.
# This is a good practice to run your application with a non-root user for security reasons.
#RUN addgroup --system app && adduser --system --group app
#USER app

ENV FLASK_CONFIG=development
ENV FLASK_APP=app.py

# For production, consider using a production-ready server like Gunicorn.
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
