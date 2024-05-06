# Deploying Django with Docker Compose

This is the finished source code for the tutorial [Deploying Django with Docker Compose](https://londonappdeveloper.com/deploying-django-with-docker-compose/).

In this tutorial, we teach you how to prepare and deploying a Django project to an AWS EC2 instance using Docker Compose.

### Step 3 : Load Initial Data (Local)

- `docker-compose run --rm app sh -c "python manage.py start_periodic_tasks"`
- `docker-compose run --rm app sh -c "python manage.py load_initial_waste_db"`
- `docker-compose run --rm app sh -c "python manage.py load_initial_auth_db"`
- `docker-compose run --rm app sh -c "python manage.py load_some_waste_transfer"` (optional)

### Step 3 : Load Initial Data (For running first time)

- `docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py start_periodic_tasks"`
- `docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py load_initial_waste_db"`
- `docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py load_initial_auth_db"`
- `docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py load_some_waste_transfer"` (optional)

## EC2 Instances Setup Guide (ec2-65-2-63-16.ap-south-1.compute.amazonaws.com)

- tutorials : `https://www.youtube.com/watch?v=mScd-Pc_pX0&pp=ygUZY2VsZXJ5IGVjMiBkb2NrZXItY29tcG9zZQ%3D%3D`
- `ssh ec2-user@ec2-65-2-63-16.ap-south-1.compute.amazonaws.com`

- `sudo yum install git -y`
- `sudo yum install docker -y`
- `sudo systemctl enable docker.service`
- `sudo systemctl start docker.service`
- `sudo usermod -aG docker ec2-user`
- `sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose`
- `sudo chmod +x /usr/local/bin/docker-compose`
- `ssh-keygen -t ed25519 -b 4096`
- `docker-compose -f docker-compose-deploy.yml up -d`
