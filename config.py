import os
from dotenv import load_dotenv

load_dotenv()


def require_env(var_name: str) -> str:
  value = os.getenv(var_name)
  if value is None or value.strip() == "":
    raise ValueError(
        f"⛔ Переменная окружения '{var_name}' не установлена в .env")
  return value


BOT_TOKEN = require_env("BOT_TOKEN")
WEATHER_API_KEY = require_env("WEATHER_API_KEY")
ADMIN_ID = int(require_env("USER_ID"))
DATABASE_URL = require_env("DATABASE_URL")
