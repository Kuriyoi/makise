# Pulls the oficcial Python 3.9.16 base image, based on Debian Bullseye (slim) 
FROM python:3.9.16-slim-bullseye

LABEL com.makise.image.title="Makise Flask Service"
LABEL com.makise.image.author="Kuriyoi"

# Directory inside the container where everything will be executed
WORKDIR /usr/src/app

# Updating the system
RUN apt update -y && apt upgrade -y

# Installs python packages needed as dependencies
RUN apt install -y python3.9-dev libpq-dev build-essential

# Removes unnecessary packages
RUN apt autoremove -y

# Updating pip (python's package manager)
RUN pip install --upgrade pip

# The project is copied from the local machine to the working directory inside
# the container, without files and directories listed on the .dockerignore file
COPY . .

# Installing the requirements needed by the project
RUN pip install --no-cache-dir -r requirements.txt
