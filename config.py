import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    PRIVATE_KEY_ENCRYPTION_KEY = os.getenv(
        "PRIVATE_KEY_ENCRYPTION_KEY"
    )

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY is missing from the .env file."
        )

    if not PRIVATE_KEY_ENCRYPTION_KEY:
        raise RuntimeError(
            "PRIVATE_KEY_ENCRYPTION_KEY is missing from the .env file."
        )

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{BASE_DIR / 'instance' / 'secure_messages.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
