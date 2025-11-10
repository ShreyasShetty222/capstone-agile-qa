import os
from dotenv import load_dotenv

# Load .env if present, then .env.example as fallback
load_dotenv(dotenv_path=".env", override=False)
load_dotenv(dotenv_path=".env.example", override=False)

CONFIG = {
    "base_url": os.getenv("BASE_URL", "https://the-internet.herokuapp.com"),
    "user": os.getenv("LOGIN_USER", "tomsmith"),
    "password": os.getenv("LOGIN_PASS", "SuperSecretPassword!"),
    "headless": str(os.getenv("HEADLESS", "true")).lower() == "true",
}
