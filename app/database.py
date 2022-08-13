# ORM for interacting with DB, but can't talk to db, need DB Driver too
from requests import session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from .config import settings
# Use Alembic for managing migrations

# exposing Username and password in code, and also have set to local postgres instance
# need a way to set this dynamically based on env, same goes for SECRET_KEY in Oauth2 - so instead use Env Vars

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to DB need a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency: Session object responsible for talking to DB, connects to DB and gets a session for sending SQL Statements and closing the connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# dB connection string - Postgres instead of SQLAlchemy
# while True:
#     print("Attempting connection to DB")
#     try:
#         connection = psycopg2.connect(host='localhost', database='fastapi_db', user='postgres', password='Postgres_098', cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Db connection successful")
#         break
#     except Exception as error:
#         print("Db Connection Failed")
#         print("Error: ", error)
#         time.sleep(2)