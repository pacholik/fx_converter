from os import getenv


DEBUG = bool(getenv("DEBUG"))

PROJECT_NAME = LOGGER_NAME = "fx_converter"
SECRET_KEY = getenv("SECRET_KEY") or "testsecretkey"

SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = True
