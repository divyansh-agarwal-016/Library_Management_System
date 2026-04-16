import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DEFAULT_DB_PATH = os.path.join(INSTANCE_DIR, "library.db")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False