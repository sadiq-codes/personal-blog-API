FROM python:3.10-slim-bullseye

EXPOSE 80/tcp

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

