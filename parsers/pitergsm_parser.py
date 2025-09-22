from .base_parser import BaseParser
from bs4 import BeautifulSoup
import re

class PiterGSMParser(BaseParser):
    def __init__(self):
        super().__init__("PiterGSM")
    
    def get_search_url(self, query):
        """Получение URL для поиска на PiterGSM"""
        return f"https://pitergsm.ru/?digiSearch=true&term={query}&params=%7Csort%3DDEFAULT"
    
    def search_products(self, query):
        """Поиск товаров на PiterGSM"""
        search_url = self.get_search_url(query)
        
        response = self.get_page(search_url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # Поиск товаров на странице
        product_elements = soup.find_all('div', class_='prodcard')
        
        for element in product_elements[:10]:  # Ограничиваем до 10 результатов
            product = self.parse_product(element)
            if product:
                products.append(product)
        
        return products
    
    def parse_product(self, product_element):
        """Парсинг информации о товаре"""
        try:
            # Название товара - улучшенный поиск
            title_elem = None
            
            # Пробуем разные варианты селекторов для названия
            title_selectors = [
                '.prodcard__name',  # Основной селектор для PiterGSM
                'a.product-item-name',
                '.product-title a',
                'h3 a',
                'h2 a',
                '.name a',
                'a[href*="/product/"]',
                'a[href*="/catalog/"]',
                '.title a'
            ]
            
            for selector in title_selectors:
                title_elem = product_element.select_one(selector)
                if title_elem:
                    break
            
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            if not title or len(title) < 3:
                return None
            
            # Цена - улучшенный поиск
            price_elem = None
            price_selectors = [
                '.prodcard__price',  # Основной селектор для PiterGSM
                'span.price',
                '.price',
                '.product-price',
                '.cost',
                '.price-current',
                '.current-price',
                '[class*="price"]'
            ]
            
            for selector in price_selectors:
                price_elem = product_element.select_one(selector)
                if price_elem:
                    break
            
            if not price_elem:
                return None
            
            price_text = price_elem.get_text(strip=True)
            # Извлекаем числовое значение цены
            price_match = re.search(r'[\d\s]+', price_text.replace(' ', ''))
            if not price_match:
                return None
            
            try:
                price = int(price_match.group().replace(' ', ''))
                if price < 100 or price > 10000000:  # Разумные пределы для цены
                    return None
            except ValueError:
                return None
            
            # Ссылка на товар
            link = title_elem.get('href')
            if link and not link.startswith('http'):
                link = f"https://pitergsm.ru{link}"
            
            return {
                'title': title,
                'price': price,
                'link': link,
                'store': self.store_name
            }
            
        except Exception as e:
            print(f"Ошибка при парсинге товара PiterGSM: {e}")
            return None

