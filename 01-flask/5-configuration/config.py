import os
from datetime import timedelta


# Base configuration class with shared defaults
class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-insecure-secret-key")

    # Custom application-level settings
    COMPANY_NAME = "CloudTech Systems"
    ITEMS_PER_PAGE = 25

    # Upload limits & Session security
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    # Database default
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///default.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev_database.db"
    ENVIRONMENT_NAME = "Development Mode"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # In-memory DB for rapid tests
    ENVIRONMENT_NAME = "Automated Testing Mode"


class ProductionConfig(Config):
    # Stricter production settings
    DEBUG = False
    TESTING = False
    # In production, require strict env variables
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:prod_pass@localhost:5432/prod_db")
    ENVIRONMENT_NAME = "Production Environment"