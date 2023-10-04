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
ENV FLASK_APP=myapp.py
# Here, we're using the Flask development server to run our application.
# For production, consider using a production-ready server like Gunicorn.
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
