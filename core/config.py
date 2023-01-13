import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    mysql_username: str = os.environ.get("MYSQL_USERNAME")
    mysql_password: str = os.environ.get("MYSQL_PASSWORD")
    mysql_database: str = os.environ.get("MYSQL_DATABASE")
    mysql_host:     str = os.environ.get("MYSQL_HOST")
    mysql_port:     int = os.environ.get("MYSQL_PORT")
    auth_secret:    str = os.environ.get("AUTH_SECRET")


settings = Settings()
