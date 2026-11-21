import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Cargar .env si existe
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

@dataclass(frozen=True)
class ServerConfig:
    host: str = os.getenv("PROD_SERVER_HOST", "fundetaxcol.co")
    ip: str = os.getenv("PROD_SERVER_IP", "149.22.88.135")
    user: str = os.getenv("PROD_SERVER_USER", "root")
    password: str = os.getenv("PROD_SERVER_PASSWORD", "2QoRhncZ")
    read_only: bool = True  # Regla Inviolable: Siempre Read-Only

@dataclass(frozen=True)
class FirebaseConfig:
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "")
    api_key: str = os.getenv("FIREBASE_API_KEY", "")
    auth_domain: str = os.getenv("FIREBASE_AUTH_DOMAIN", "")
    database_url: str = os.getenv("FIREBASE_DATABASE_URL", "")

@dataclass(frozen=True)
class AppConfig:
    env: str = os.getenv("APP_ENV", "development")
    version: str = os.getenv("APP_VERSION", "3.0.0")
    build_number: int = int(os.getenv("APP_BUILD_NUMBER", "1"))
    base_dir: Path = BASE_DIR
    reference_dir: Path = BASE_DIR / "reference"
    server: ServerConfig = ServerConfig()
    firebase: FirebaseConfig = FirebaseConfig()

config = AppConfig()
