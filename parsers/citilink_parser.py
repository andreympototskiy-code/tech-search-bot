from .base_parser import BaseParser
from bs4 import BeautifulSoup
import re


class CitilinkParser(BaseParser):
    def __init__(self):
        super().__init__("Ситилинк")

    def search_products(self, query):
        """Поиск товаров на Ситилинк"""
        search_url = f"https://www.citilink.ru/search/?text={query}"

        response = self.get_page(search_url)
        if not response:
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        products = []

        # Поиск товаров на странице
        product_elements = soup.find_all("div", class_="product-card")

        for element in product_elements[:10]:
            product = self.parse_product(element)
            if product:
                products.append(product)

        return products

    def parse_product(self, product_element):
        """Парсинг информации о товаре"""
        try:
            # Название товара
            title_elem = product_element.find("a", class_="product-title")
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)

            # Цена
            price_elem = product_element.find("span", class_="price")
            if not price_elem:
                return None

            price_text = price_elem.get_text(strip=True)
            price_match = re.search(r"[\d\s]+", price_text.replace(" ", ""))
            if not price_match:
                return None

            price = int(price_match.group().replace(" ", ""))

            # Ссылка на товар
            link = title_elem.get("href")
            if link and not link.startswith("http"):
                link = f"https://www.citilink.ru{link}"

            return {
                "title": title,
                "price": price,
                "link": link,
                "store": self.store_name,
            }

        except Exception as e:
            print(f"Ошибка при парсинге товара Ситилинк: {e}")
            return None


