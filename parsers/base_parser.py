import requests
from bs4 import BeautifulSoup
import time
import random
from abc import ABC, abstractmethod

class BaseParser(ABC):
    def __init__(self, store_name):
        self.store_name = store_name
        self.session = requests.Session()
        
        # Реалистичные заголовки для обхода блокировок
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        })
    
    def get_page(self, url, max_retries=3):
        """Получение страницы с повторными попытками"""
        for attempt in range(max_retries):
            try:
                # Задержка между запросами 20 секунд
                from config.settings import REQUEST_DELAY_SECONDS
                delay = REQUEST_DELAY_SECONDS
                print(f"Задержка {delay} сек перед запросом к {self.store_name}")
                time.sleep(delay)
                
                # Добавляем Referer для реалистичности
                if 'pitergsm.ru' in url:
                    self.session.headers.update({'Referer': 'https://pitergsm.ru/'})
                elif 'world-devices.ru' in url:
                    self.session.headers.update({'Referer': 'https://world-devices.ru/'})
                elif 'gsm-store.ru' in url:
                    self.session.headers.update({'Referer': 'https://gsm-store.ru/'})
                
                response = self.session.get(url, timeout=15, allow_redirects=True)
                response.raise_for_status()
                
                # Исправляем проблему с кодировкой для некоторых сайтов
                if 'pitergsm.ru' in url and response.headers.get('content-encoding') == 'br':
                    # Для PiterGSM принудительно устанавливаем UTF-8
                    response.encoding = 'utf-8'
                    # Дополнительно декодируем содержимое
                    try:
                        import brotli
                        if response.content:
                            response._content = brotli.decompress(response.content)
                    except:
                        pass
                
                return response
            except Exception as e:
                print(f"Ошибка при получении страницы {url} (попытка {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    return None
                # Увеличенная задержка между попытками
                time.sleep(random.uniform(5, 10))
        return None
    
    def get_search_url(self, query):
        """Получение URL для поиска"""
        # Базовый метод, переопределяется в наследниках
        return f"https://example.com/search?q={query}"

    @abstractmethod
    def search_products(self, query):
        """Поиск товаров по запросу"""
        pass

    @abstractmethod
    def parse_product(self, product_element):
        """Парсинг информации о товаре"""
        pass

