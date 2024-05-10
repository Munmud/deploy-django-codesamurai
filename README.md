## About Us

- Team Name : `RU LEGION`
- Member1 : `Moontasir Mahmood` - `moontasir042@gmail.com`
- Member2 : `Md Atikur Rahman` - `md.atik.dev@gmail.com`
- Member3 : `Abdullah Al Ghalib` - `abdullah.ice.ru@gmail.com`

## Getting started

### Step-1 : To start project, install docker and from command line run:

- `docker-compose up --build`

The API will then be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Step-2 : Load Initial Data

#### Localhost

- `docker-compose run --rm app sh -c "python manage.py start_periodic_tasks"`
- `docker-compose run --rm app sh -c "python manage.py load_initial_waste_db"`
- `docker-compose run --rm app sh -c "python manage.py load_initial_auth_db"`
- `docker-compose run --rm app sh -c "python manage.py load_some_waste_transfer"` (optional)

#### Production

- `docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py start_periodic_tasks"`
- `docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py load_initial_waste_db"`
- `docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py load_initial_auth_db"`
- `docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py load_some_waste_transfer"` (optional)

## Deployment Guide for development

### EC2 Instances Setup Guide (ec2-65-2-63-16.ap-south-1.compute.amazonaws.com)

- tutorials : `https://www.youtube.com/watch?v=mScd-Pc_pX0&pp=ygUZY2VsZXJ5IGVjMiBkb2NrZXItY29tcG9zZQ%3D%3D`
- `ssh ec2-user@ec2-65-2-63-16.ap-south-1.compute.amazonaws.com`
- `cd deploy-django-codesamurai`
- `docker-compose -f docker-compose-deploy.yml down --volumes`
- `git pull`
- `docker-compose -f docker-compose-deploy.yml build`
- `docker-compose -f docker-compose-deploy.yml up`

- `sudo yum install git -y`
- `sudo yum install docker -y`
- `sudo systemctl enable docker.service`
- `sudo systemctl start docker.service`
- `sudo usermod -aG docker ec2-user`
- `sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose`
- `sudo chmod +x /usr/local/bin/docker-compose`
- `ssh-keygen -t ed25519 -b 4096`
- `docker-compose -f docker-compose-deploy.yml up -d`
