# Makise Online Shop
## Description
This project is an online manga shop. It is a web application developed in Python using the Flask framework.

## Installation
### Requirements
You need to have Docker and Docker Compose installed on your machine. If you don't have them, you can install them from
the following links:

- [Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Linux](https://docs.docker.com/engine/install/)

You just need to follow the steps on the link of your operating system. If you are using Linux, it is recommended to
install Docker Engine instead of Docker Desktop. You can choose your distro in the left menu of the previous link.

### Steps
1. Clone the repository to your desired directory
2. Open a terminal in the root directory of the project
3. Run the following command: `docker compose -f makise-compose-dev up -d`. If you have an old Docker version, you may
   need to run `docker-compose -f makise-compose-dev up -d`
4. Open a browser and go to `localhost:5000`