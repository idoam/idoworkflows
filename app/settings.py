import os
from os.path import join
from pathlib import Path

from dotenv import load_dotenv

# Load env file
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = join(BASE_DIR.parent, ".env")
load_dotenv(dotenv_path)

KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "localhost").split(",")
