import os

import redis

from pydantic import BaseSettings


class Settings(BaseSettings):
    mysql_username: str = os.environ.get("MYSQL_USERNAME")
    mysql_password: str = os.environ.get("MYSQL_PASSWORD")
    mysql_database: str = os.environ.get("MYSQL_DATABASE")
    mysql_host    : str = os.environ.get("MYSQL_HOST")
    mysql_port    : int = os.environ.get("MYSQL_PORT")
    auth_secret   : str = os.environ.get("AUTH_SECRET")
    redis_database: int = os.environ.get("REDIS_DATABASE")
    redis_host    : str = os.environ.get("REDIS_HOST")
    redis_port    : int = os.environ.get("REDIS_PORT")
    temp_token_db : int = os.environ.get("REDIS_TEMP_TOKEN_DB")
    server_url    : str = os.environ.get("SERVER_URL")


settings = Settings()


def load_redis(
    db: int = settings.redis_database
):
    return redis.StrictRedis(
                            host=settings.redis_host,
                            port=settings.redis_port,
                            db=db,
                            charset="utf-8",
                            decode_responses=True
                         )
