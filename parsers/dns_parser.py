from .base_parser import BaseParser
from bs4 import BeautifulSoup
import re

class DNSParser(BaseParser):
    def __init__(self):
        super().__init__("DNS")
    
    def search_products(self, query):
        """Поиск товаров на DNS"""
        search_url = f"https://www.dns-shop.ru/search/?q={query}"
        
        response = self.get_page(search_url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        # Поиск товаров на странице
        product_elements = soup.find_all('div', class_='catalog-product')
        
        for element in product_elements[:10]:
            product = self.parse_product(element)
            if product:
                products.append(product)
        
        return products
    
    def parse_product(self, product_element):
        """Парсинг информации о товаре"""
        try:
            # Название товара
            title_elem = product_element.find('a', class_='catalog-product__name')
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            
            # Цена
            price_elem = product_element.find('div', class_='product-buy__price')
            if not price_elem:
                return None
            
            price_text = price_elem.get_text(strip=True)
            price_match = re.search(r'[\d\s]+', price_text.replace(' ', ''))
            if not price_match:
                return None
            
            price = int(price_match.group().replace(' ', ''))
            
            # Ссылка на товар
            link = title_elem.get('href')
            if link and not link.startswith('http'):
                link = f"https://www.dns-shop.ru{link}"
            
            return {
                'title': title,
                'price': price,
                'link': link,
                'store': self.store_name
            }
            
        except Exception as e:
            print(f"Ошибка при парсинге товара DNS: {e}")
            return None


