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