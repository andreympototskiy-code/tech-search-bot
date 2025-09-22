import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot настройки
# Токены должны быть установлены в переменных окружения или .env файле
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Проверка наличия токенов
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен! Создайте .env файл с токеном.")
if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID не установлен! Создайте .env файл с Chat ID.")

# Настройки поиска
SEARCH_INTERVAL_HOURS = 0  # Отключен автоматический поиск
MAX_RESULTS = 3
REQUEST_DELAY_SECONDS = 20  # Задержка между запросами 20 секунд

# База данных
DATABASE_PATH = "data/search_results.db"

# Веб-интерфейс
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
DEBUG = True

# Магазины для поиска (только рабочие)
STORES = [
    {
        "name": "PiterGSM",
        "url": "https://pitergsm.ru/",
        "search_url": "https://pitergsm.ru/?digiSearch=true&term={query}&params=%7Csort%3DDEFAULT",
        "parser": "pitergsm",
    },
    {
        "name": "World Devices",
        "url": "https://world-devices.ru/",
        "search_url": "https://world-devices.ru/search/?search={query}&description=true",
        "parser": "world_devices",
    },
    # Временно отключены заблокированные магазины:
    # - GSM Store (403 Forbidden)
    # - DNS, М.Видео, Эльдорадо, Ситилинк (заблокированы)
]
