#!/usr/bin/env python3
"""
Отладка HTML структуры для понимания селекторов
"""

import sys
import os
sys.path.append('.')

from parsers.world_devices_parser import WorldDevicesParser
import requests
from bs4 import BeautifulSoup

def debug_html_structure():
    """Отладка HTML структуры"""
    print("🔍 Отладка HTML структуры World Devices")
    print("=" * 60)
    
    # Создаем парсер
    parser = WorldDevicesParser()
    
    # Тестовый запрос
    query = "iPhone 15 PRO 256gb"
    search_url = f"https://world-devices.ru/search/?search={query}&description=true"
    
    # Получаем страницу
    response = parser.get_page(search_url)
    if not response:
        print("❌ Не удалось получить страницу")
        return
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Находим элементы товаров
    product_elements = soup.select('.product-layout')
    print(f"📦 Найдено элементов товаров: {len(product_elements)}")
    
    if product_elements:
        first_product = product_elements[0]
        print(f"\n🔍 Структура первого товара:")
        print(f"HTML: {str(first_product)[:500]}...")
        
        print(f"\n📋 Все классы первого товара:")
        classes = first_product.get('class', [])
        for cls in classes:
            print(f"  - {cls}")
        
        print(f"\n🔍 Все ссылки в первом товаре:")
        links = first_product.find_all('a')
        for i, link in enumerate(links):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            print(f"  {i+1}. href='{href}' text='{text[:50]}...'")
        
        print(f"\n💰 Все элементы с ценой:")
        price_elements = first_product.find_all(text=lambda text: text and 'р.' in str(text))
        for i, elem in enumerate(price_elements):
            print(f"  {i+1}. {elem}")
        
        print(f"\n📝 Все заголовки:")
        headers = first_product.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for i, header in enumerate(headers):
            text = header.get_text(strip=True)
            print(f"  {i+1}. <{header.name}> {text}")
        
        print(f"\n🎯 Пробуем разные селекторы:")
        selectors_to_test = [
            '.caption h4 a',
            '.caption a',
            'h4 a',
            'a[href]',
            '.product-name',
            '.title',
            '.name'
        ]
        
        for selector in selectors_to_test:
            elements = first_product.select(selector)
            if elements:
                print(f"✅ '{selector}': {len(elements)} элементов")
                for elem in elements:
                    text = elem.get_text(strip=True)
                    href = elem.get('href', '')
                    print(f"    - text: '{text[:30]}...' href: '{href[:30]}...'")
            else:
                print(f"❌ '{selector}': не найдено")

if __name__ == "__main__":
    debug_html_structure()



