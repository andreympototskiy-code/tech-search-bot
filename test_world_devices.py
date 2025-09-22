#!/usr/bin/env python3
"""
Тестирование парсера World Devices
"""

import sys
import os
sys.path.append('.')

from parsers.world_devices_parser import WorldDevicesParser
import requests
from bs4 import BeautifulSoup

def test_world_devices_parsing():
    """Тестирование парсинга World Devices"""
    print("🔍 Тестирование World Devices")
    print("=" * 50)
    
    # Создаем парсер
    parser = WorldDevicesParser()
    
    # Тестовый запрос
    query = "iPhone 15 PRO 256gb"
    search_url = f"https://world-devices.ru/search/?search={query}&description=true"
    
    print(f"📡 URL: {search_url}")
    
    # Получаем страницу
    response = parser.get_page(search_url)
    if not response:
        print("❌ Не удалось получить страницу")
        return
    
    print(f"✅ Страница получена, размер: {len(response.text)} символов")
    
    # Парсим HTML
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Ищем элементы товаров
    product_elements = soup.select('.product-layout')
    print(f"📦 Найдено элементов товаров: {len(product_elements)}")
    
    if product_elements:
        print("\n🔍 Анализ первого товара:")
        first_product = product_elements[0]
        
        # Название
        title_elem = first_product.select_one('.caption h4 a')
        if title_elem:
            title = title_elem.get_text(strip=True)
            print(f"📝 Название: {title}")
        else:
            print("❌ Название не найдено")
            print("🔍 Доступные элементы с классом 'caption':")
            caption_elements = first_product.select('.caption')
            for i, elem in enumerate(caption_elements):
                print(f"  {i+1}. {elem}")
        
        # Цена
        price_elem = first_product.select_one('.price-new')
        if not price_elem:
            price_elem = first_product.select_one('.price')
        
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            print(f"💰 Цена: {price_text}")
        else:
            print("❌ Цена не найдена")
            print("🔍 Доступные элементы с ценой:")
            price_elements = first_product.select('[class*="price"]')
            for i, elem in enumerate(price_elements):
                print(f"  {i+1}. {elem}")
        
        # Ссылка
        link_elem = first_product.select_one('.caption h4 a')
        if link_elem:
            link = link_elem.get('href')
            print(f"🔗 Ссылка: {link}")
        else:
            print("❌ Ссылка не найдена")
    
    # Тестируем парсер
    print("\n🧪 Тестирование парсера:")
    results = parser.search_products(query)
    print(f"📊 Результатов парсера: {len(results)}")
    
    if results:
        print("✅ Парсер работает!")
        for i, product in enumerate(results[:3]):
            print(f"  {i+1}. {product['title'][:50]}... - {product['price']} руб.")
    else:
        print("❌ Парсер не находит товары")
        
        # Пробуем разные селекторы
        print("\n🔍 Поиск альтернативных селекторов:")
        alternative_selectors = [
            '.product-item',
            '.product-card', 
            '.item',
            '[data-product]',
            '.goods-item'
        ]
        
        for selector in alternative_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"✅ Найдены элементы '{selector}': {len(elements)}")

if __name__ == "__main__":
    test_world_devices_parsing()




