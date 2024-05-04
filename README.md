# Deploying Django with Docker Compose

This is the finished source code for the tutorial [Deploying Django with Docker Compose](https://londonappdeveloper.com/deploying-django-with-docker-compose/).

In this tutorial, we teach you how to prepare and deploying a Django project to an AWS EC2 instance using Docker Compose.

## EC2 Instances Command

- `ssh ec2-user@ec2-65-2-63-16.ap-south-1.compute.amazonaws.com`

- `sudo yum install git -y`
- `sudo yum install docker -y`
- `sudo systemctl enable docker.service`
- `sudo systemctl start docker.service`
- `sudo usermod -aG docker ec2-user`
- `sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose`
- `sudo chmod +x /usr/local/bin/docker-compose`
