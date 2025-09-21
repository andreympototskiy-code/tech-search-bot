import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot настройки
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8443193400:AAEiK_YvNHrgvQwUOJtI5Hp-OHoo-_-ucj0')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '312949483')

# Настройки поиска
SEARCH_INTERVAL_HOURS = 0  # Отключен автоматический поиск
MAX_RESULTS = 3

# База данных
DATABASE_PATH = 'data/search_results.db'

# Веб-интерфейс
WEB_HOST = '0.0.0.0'
WEB_PORT = 5000
DEBUG = True

# Магазины для поиска
STORES = [
    {
        'name': 'PiterGSM',
        'url': 'https://pitergsm.ru/',
        'search_url': 'https://pitergsm.ru/?digiSearch=true&term={query}&params=%7Csort%3DDEFAULT',
        'parser': 'pitergsm'
    },
    {
        'name': 'World Devices',
        'url': 'https://world-devices.ru/',
        'search_url': 'https://world-devices.ru/search/?search={query}&description=true',
        'parser': 'world_devices'
    },
    {
        'name': 'GSM Store',
        'url': 'https://gsm-store.ru/',
        'search_url': 'https://gsm-store.ru/?digiSearch=true&term={query}&params=%7Csort%3DDEFAULT',
        'parser': 'gsm_store'
    },
    {
        'name': 'DNS',
        'url': 'https://www.dns-shop.ru/',
        'search_url': 'https://www.dns-shop.ru/search/?q={query}',
        'parser': 'dns'
    },
    {
        'name': 'М.Видео',
        'url': 'https://www.mvideo.ru/',
        'search_url': 'https://www.mvideo.ru/products/search?q={query}',
        'parser': 'mvideo'
    },
    {
        'name': 'Эльдорадо',
        'url': 'https://www.eldorado.ru/',
        'search_url': 'https://www.eldorado.ru/search/?q={query}',
        'parser': 'eldorado'
    },
    {
        'name': 'Ситилинк',
        'url': 'https://www.citilink.ru/',
        'search_url': 'https://www.citilink.ru/search/?text={query}',
        'parser': 'citilink'
    }
]

