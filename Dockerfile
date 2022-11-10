## Set base image (host OS)
#FROM python:3.10-alpine
#
## By default, listen on port 5000
#EXPOSE 5000/tcp
#
## Set the working directory in the container
#WORKDIR /app
#
## Copy the dependencies file to the working directory
#COPY requirements.txt .
#
## Install any dependencies
#RUN pip install -r requirements.txt
#
## Copy the content of the local src directory to the working directory
#COPY blog.py .
#
## Specify the command to run on container start
#CMD [ "python", "./blog.py" ]

FROM python:3.10-slim-bullseye

EXPOSE 5000/tcp

ENV FLASK_APP blog.py
ENV FLASK_CONFIG development

#RUN adduser -D blogy
#USER blogy

WORKDIR /blog

#RUN python -m venv venv

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory

#COPY blog.py settings.py spaces.py fake.py routes.py ./
COPY . .

# runtime configuration
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

