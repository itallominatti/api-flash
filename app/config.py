from pydantic import BaseSettings, validator
from os import getenv as env


class Settings(BaseSettings):
    APP_ENV: str = env("ENV")

    if APP_ENV == "Dev":
        CORS_ORIGINS = ["*"]

        DB_INT_NAME = env("DEV_DB_INT_NAME")
        DB_INT_USER = env("DEV_DB_INT_USER")
        DB_INT_PASS = env("DEV_DB_INT_PASS")
        DB_INT_HOST = env("DEV_DB_INT_HOST")

        FLASH_PEGASUS_API_URL = env("FLASH_PEGASUS_API_URL_DEV")
        FLASH_PEGASUS_AUTH_USER = env("FLASH_PEGASUS_AUTH_USER_DEV")
        FLASH_PEGASUS_AUTH_PASSWORD = env("FLASH_PEGASUS_AUTH_PASSWORD_DEV")

        FLASH_API_TOKEN_URL = env("FLASH_API_TOKEN_URL_DEV")
        FLASH_API_CONSULTA_URL = env("FLASH_API_CONSULTA_URL_DEV")

    elif APP_ENV == "Hom":
        CORS_ORIGINS = ["*"]

        DB_INT_NAME = env("HOM_DB_INT_NAME")
        DB_INT_USER = env("HOM_DB_INT_USER")
        DB_INT_PASS = env("HOM_DB_INT_PASS")
        DB_INT_HOST = env("HOM_DB_INT_HOST")

        FLASH_PEGASUS_API_URL = env("FLASH_PEGASUS_API_URL_HOM")
        FLASH_PEGASUS_AUTH_USER = env("FLASH_PEGASUS_AUTH_USER_HOM")
        FLASH_PEGASUS_AUTH_PASSWORD = env("FLASH_PEGASUS_AUTH_PASSWORD_HOM")

        FLASH_API_TOKEN_URL = env("FLASH_API_TOKEN_URL_HOM")
        FLASH_API_CONSULTA_URL = env("FLASH_API_CONSULTA_URL_HOM")

    elif APP_ENV == "Prod":
        CORS_ORIGINS = ["*"]

        DB_INT_NAME = env("PROD_DB_INT_NAME")
        DB_INT_USER = env("PROD_DB_INT_USER")
        DB_INT_PASS = env("PROD_DB_INT_PASS")
        DB_INT_HOST = env("PROD_DB_INT_HOST")

        FLASH_PEGASUS_API_URL = env("FLASH_PEGASUS_API_URL_PROD")
        FLASH_PEGASUS_AUTH_USER = env("FLASH_PEGASUS_AUTH_USER_PROD")
        FLASH_PEGASUS_AUTH_PASSWORD = env("FLASH_PEGASUS_AUTH_PASSWORD_PROD")

        FLASH_API_TOKEN_URL = env("FLASH_API_TOKEN_URL_PROD")
        FLASH_API_CONSULTA_URL = env("FLASH_API_CONSULTA_URL_PROD")

    class Config:
        case_sensitive = True


settings = Settings()