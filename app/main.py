from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
# bind the models
# creates tables if they're not present in DB
# Don't actually need this with Alembic migrations
# models.Base.metadata.create_all(bind=engine)
# CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# make user of the routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# development:
# use uvicorn app.main:app --reload to run local server
# url/docs and url/redocs can provide documentation for the api

# path operation: 
# @app.[method]("[path]")
#   def [function]()

# JWT tokens are unencrypted tokens for authorization to the API
# Header specifies the algorithm to be used, type is JWT
# Payload is utimately up to you, don't want passwords or secrets so things like id of the user, to be extracted for info re the user
# Signiture is a combination of Header, Payload and Secret on the API client, pass into signing algorithm and returns a signiture to determine if the token is valid
# The signiture in the token is generated with a header, payload and secret; if they change the signiture or payload it won't match the other on the API server without using the Hashing function, Signiture ensures the Token hasn't been tampered with
# in postman can go to tests and set the JWT token as an env variable - see POST/login TESTS tab
# can then similarly set the auth/bearer token value as {{var}}

# CORS policy https://youtu.be/0sOvCWFmrtA?t=40659
# CORS allows you to make requests from one domain to server on another domain, API by default only allows browsers on the same domain as our server to make requests to it

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Can allow domains, HTTP Methods, headers


# Postgres installation comes with one db called 'postgres'
# when you connect to postgres you must specify a DB

# Git
# Git - first define a gitignore file for files and folders you don't want checked in like .env, venv/, __pycache__
# not uploading venv means you don't upload packages, need to inform other users about packages and dependencies which we would need
# pip freeze > requirements.txt creates a txt file of packages to install, pip install -r requirements.txt
# https://youtu.be/0sOvCWFmrtA?t=41570
# git config --global user.email/name 'x'
# git commit -m 'name'
# echo "# example-fastapi" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/RowanRibbit/example-fastapi.git
# git push -u origin main

# Now deploy the application; First is Heroku
# heroku login
# https://serene-peak-42523.herokuapp.com/docs
# heroku create {APP-name} - I forgot to add the name
# heroku adds a branch heroku to our github
# git push heroku main
# heroku doesn't know to run app.main:app like we do with uvicorn
# create Procfile in the root dir
# web: uvicorm app.main:app --host=0.0.0.0 --port=${PORT:-5000}
# have to provide the host IP, and the port flag to run on. Don't provide reload as this should be in production. We don't know the port, but will be passed as an Env var, so take any env var PORT as assign it, with a default value of 5000
# issue with our environment variables - in dev we used the .env file but in production we didn't check .env into Git
# need to configure a Postgres DB on heroku, then add the env vars

# Heroku Postgres
# heroku addons:create heroku-postgresql:hobby-dev
# go to the App Dashboard and save the details
# go to settings>Config Vars to set Env Vars
# restart the heroku instance
# heroku ps:restart
# heroku logs -t

# However, now there are issues with the DB - SQL in the logs, some error with the SQL, deployed a new instance of postgres but we didn't initialise the DB
# in dev environment used alembic to manage our DB, and to keep it up to date ran alembic upgrade head
# on the instance, run alembic upgrade head in Heroku - can use heroku run 'alembic upgrade head'

# deploying to an ubuntu server https://youtu.be/0sOvCWFmrtA?t=43531
# DigitalOcean - relatively cheap
# 'Get started with a droplet' > Ubuntu distribution
# 'Regular Intel with SSD', select your datacentre, rest can be default (SSH Keys if familiar or password if preferred)
# Specific hostname, and create

# Displays a public IP to connect to Ubuntu VM
# CMD > ssh {username_of_root_user}@{ip_address} (root@ip), password of VM
# ls for contents of dir
# update all of the install packages - 'sudo apt update && sudo apt upgrade -y'
# -y autofills yes
# install extra packages python3 --version, sudo apt install python
# install pip, pip --version pip3 --version, sudo apt install python3-pip
# use pip to install venv
# sudo pip3 install virtualenv
# install postgres - sudo apt install postgresql postgresql-contrib -y
# before trying to connect virtually, use the postgres console
# psql -U {username} (Postgres) 
# Postgres on Ubuntu Peer Authentication is not Local - default config, takes the logged in Ubuntu user and tries to log in; Postgres will only allow an Ubuntu user called Postgres to login, but postgres knows this so creates a user called Postgres
# change to user Postgres 'su - postgres'
# now psql -U postgres will show the postgres console
# create password '\password postgres'
# to exit postgres console \q
# exit in console returns to root user
# cd /etc/postgresql/{version#}/main (etc where any application on Ubuntu is usually installed)
# sudo vi postgresql.conf, scroll down and see Connections and Auth settings
# localhost can only connect at the moment, under settings listen_addresses = '{ip_addresses}' i.e., '*' for all
# sudo vi pg_hba.conf, scroll down to default config, for local users don't use Peer use md5 where says Peer
# change for any DB any User local connections has 127.0.0.1 which is local, change to 0.0.0.0/0 for IPv4 and IPv6 ::/0
# have to restart the application - 'systemctl restart postgresql'
# psql -U postgres from root prompts for password
# PGAdmin - servers, create, connection provide the IP address, password

# Generally don't want to be logged in as Root user - create user with Root privilages but won't be the root user. Non-root user will be responsible for starting our Python app
# adduser {name}
# su - {name}
# ssh {name}@{ip} will log in as that user
# usermod -aG sudo {name} to grant sudo access (root access)
# pwd is dir, default dir. cd ~ to home dir or cd/home/{name}
# mkdir app
# cd app
# virtualenv venv
# ls -la to check it exists
# source venv/bin/activate, will show (venv), deactivate to exit
# mkdir src
# cd src/
# code is on github, go to url for repo
# 'git clone {url} .' to install in this dir without creating a new dir
# reactivate venv - 'cd ..', 'source venv/bin/activate'
# use requirements to install packages - 'pip install -r requirements.txt', error libpq-fe.h and search to see how to install it
# deactivate venv, 'sudo apt install libpq-dev'
# back to venv, run command to install reqs
# try and start app - uvicorn app.main:app, but Env Vars not set

# Environment Vars
# 'export {ENV_NAME}={VALUE}'
# printenv prints environment vars
# can do manually, can remove unset {ENV_NAME}
# cd ~
# touch .env
# vi .env, provide a list on Env Vars
# export {NAME}={VALUE}, save the file
# source .env, sets all the Env Vars
# but in this case, open .env file and delete the contents, the Copy/Paste the .env from local and fix it
# 'set -o allexport; source /home/{name}/.env; set +o allexport', but when you reboot the machine lose Env Vars
# To have them persist through reboot, ls -la, will go to .profile file
# vi .profile, and below the bottom of the file paste the 'set -o...' cmd in then :wq to exit. This will cause any time to login to this user, will run this cmd
# .env in home directory, not the app dir to keep it separate
# update the .env files to production, not dev
# vi .env
# update the production password, secret key and access token
# reactivate env. cd app/, 'source venv/bin/activate'. In production and we set up Alembic cd src/
# alembic upgrade head rolls up to the latest migration
# cd app/src/ uvicorn --host 0.0.0.0 (--port {port}) app.main:app
# {ip}:8000
# will use gunicorn, a process manager
# pip install gunicorn in venv
# (may need pip install httptools, pip install uvloop)
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
# can pip freeze and update your requirements.txt for git
# gunicorn starts 4 worker nodes 
# ps -aef | grep -i gunicorn shows the 5 processes started, parent and 4 child

# have to automate the process of starting the workers and make it a background process
# cd /etc/systemd/system show the services on the machine
# create a couple of files, gunicorn.service
# https://github.com/Sanjeev-Thiyagarajan/fastapi-course/blob/main/gunicorn.service
#  After=network.target - tells ubuntu when to run it; wait for network then start
# What user will run the service, Group same as the user
# Working Directory to the dir of the App ~app/src/ 'pwd'
# Environment='PATH={bin path}'
# ExecStart={path to gunicorn command}
# Install is a default config
# cd /etc/systemmd/system/
# sudo vi {servicename.service}
# systemctl start {servicename}
# servicefile needs access to Environment Variables, aren't accessible in a service
# in service file 'EnvironmentFile=/home/{name}/.env'
# make sure our service starts on reboot
# system ctlstatus {name}, disabled; means no, so sudo systemctl enable api will change to enabled

# NGINX https://youtu.be/0sOvCWFmrtA?t=47150
# High performance proxy webserver that can act as a proxy, can handle SSL termination
# Send our HTTP Request to NGINX server, then NGINX performs tasks like SSL offload optimised for these tasks, instead of putting the load on our API
# Any request sent to NGINX, if HTTPS takes it and forwards it as HTTP

# sudo apt install nginx -y
# systemctl start nginx, now the server IP address has the nginx splash
# cd /etc/nginx/sites-available/, ls should contain default config file
# will change the config, change the location block to allow it to act as a proxy (proxy_pass http://localhost:8000) - specify the IP address and port to forward 
# https://github.com/Sanjeev-Thiyagarajan/fastapi-course/blob/main/nginx
# systemctl restart nginx, now we can see the API again at the uri
# now need to set up the website to use HTTPS, need a domain name or a self signed certificate
# .xyz domains are the cheapest, namecheap.com, godaddy, amazon etc
# Point the DomainName to Domain Registrar. Custom DNS > ns1.digitalocean.com, ns2...
# Create A record: root of the domain - networking on digitalocean, add the domain
# Create a subdomain: CNAME - www, @
# Now we have a domain, can set up SSL

# Setting up SSL: certbot
# Get Certbot instructions, NGINX, Ubuntu
# snap --version, if not installed install it
# sudo snap install --classic certbot
# sudo certbox --nginx to automatically configure NGINX for you, provide an email address, specify the domain names, {url} www.{url}
# main change to our config is the server block of NGINX config for SSL configuration, and a server block that redirects HTTP to HTTPS, returns a 301 redirect
# want to set up nginx to see if it's set up to start on reboot, systemctl status nginx, if disabled systemctl enable nginx

# Set up a firewall on the machine, only open a port you are using
# sudo ufw status (firewall), need to set up rules
# sudo ufw allow http
# sudo ufw allow https
# sudo ufw allow ssh
# sudo ufw allow 5432 (don't need to allow this port, as app is running on the local machine), but if you want to connect to your box remotely with PGAdmin will need to add this rule
# sudo ufw enable
# sudo ufw status will show the ports available

# Making changes and pushing changes
# git add --all
# git commit -m 'message'
# git push origin main (+- heroku main)
# on Ubuntu
# cd app/src/
# git pull, pulls the latest changes
# if changed requirements.txt, pip install -r requirements.txt
# sudo systemctl restart api

# Docker https://youtu.be/0sOvCWFmrtA?t=48407
# How to make an image for a FastAPI Docker Container
# Search for Python > Official Python image (different versions and types), start with the base python image, installing dependencies
# create file Dockerfile
# 'docker build -t {tag} fastapi .'
# builds the docker image
# 'docker image ls' shows the docker images
# can use 'docker run', but instead user 'docker compse up' to write out the flags in a file and automatically spin up containers
# create docker-compose.yml
# 'docker compose up -d', creates container name {dir}_{servicename}_{#}
# can check logs - docker logs {name}
# pass in env vars in yml