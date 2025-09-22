from .base_parser import BaseParser
from bs4 import BeautifulSoup
import re

class WorldDevicesParser(BaseParser):
    def __init__(self):
        super().__init__("World Devices")
    
    def get_search_url(self, query):
        """Получение URL для поиска на World Devices"""
        return f"https://world-devices.ru/search/?search={query}&description=true"
    
    def search_products(self, query):
        """Поиск товаров на World Devices"""
        search_url = self.get_search_url(query)
        
        response = self.get_page(search_url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # Поиск товаров на странице - используем правильный селектор
        product_elements = soup.select('.product-layout')
        
        print(f"Найдено элементов товаров: {len(product_elements)}")
        
        for element in product_elements[:10]:
            product = self.parse_product(element)
            if product:
                products.append(product)
        
        return products
    
    def parse_product(self, product_element):
        """Парсинг информации о товаре"""
        try:
            # Название товара - различные возможные селекторы
            title_elem = None
            
            # Пробуем разные варианты селекторов для названия
            title_selectors = [
                '.product-thumb__name',  # Основной селектор для World Devices
                'a[href*="/smartfony/"]',
                '.caption h4 a',
                '.caption h3 a',
                '.caption h2 a',
                '.caption a',
                'h4 a',
                'h3 a',
                'h2 a',
                '.product-name a',
                '.product-title a',
                '.product-item-name',
                '.name a',
                'a[href*="/product/"]',
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
            
            # Цена - различные возможные селекторы
            price_elem = None
            price_selectors = [
                '.product-thumb__price',  # Основной селектор для World Devices
                '.price-new',
                '.price',
                '.product-price',
                '.cost',
                '.price-current',
                '.current-price',
                '[class*="price"]',
                '.value',
                'text'  # Ищем по тексту, содержащему "р."
            ]
            
            for selector in price_selectors:
                if selector == 'text':
                    # Ищем текст с ценой
                    price_texts = product_element.find_all(string=lambda text: text and 'р.' in str(text))
                    if price_texts:
                        price_elem = price_texts[0].parent  # Берем родительский элемент
                        break
                else:
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
                link = f"https://world-devices.ru{link}"
            
            return {
                'title': title,
                'price': price,
                'link': link,
                'store': self.store_name
            }
            
        except Exception as e:
            print(f"Ошибка при парсинге товара World Devices: {e}")
            return None
