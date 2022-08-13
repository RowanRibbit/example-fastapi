from pydantic import BaseSettings

# pydantic makes these case insensitive
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
# pydantic reads the Env Vars and stores in Settings
# if Var is missing or wrong type (reads as string and casts), throws an error