from os import environ


def construct_database_uri():
    user = environ["POSTGRES_USER"]
    password = environ["POSTGRES_PASSWORD"]
    database = environ["POSTGRES_DB"]
    host = environ.get("POSTGRES_HOST", "localhost")
    port = environ.get("POSTGRES_PORT", 5432)
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def get_secret_key():
    return environ["WEBAPP_SECRET_KEY"]


class Config:
    DEBUG = True
    SECRET_KEY = get_secret_key()
    SESSION_COOKIE_HTTPONLY = True
    SESSION_PROTECTION = "strong"
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = construct_database_uri()
