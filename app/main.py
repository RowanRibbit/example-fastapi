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