#!/usr/bin/env python3
"""
Быстрый тест исправленных парсеров
"""

import sys
import os
sys.path.append('.')

from parsers.world_devices_parser import WorldDevicesParser
from bs4 import BeautifulSoup

def quick_test_world_devices():
    """Быстрый тест World Devices"""
    print("🔍 Быстрый тест World Devices")
    print("-" * 40)
    
    parser = WorldDevicesParser()
    query = "iPhone 15 PRO 256gb"
    
    # Получаем страницу
    response = parser.get_page(f"https://world-devices.ru/search/?search={query}&description=true")
    if not response:
        print("❌ Не удалось получить страницу")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.select('.product-layout')
    
    print(f"📦 Найдено товаров: {len(products)}")
    
    if products:
        first = products[0]
        
        # Тестируем новые селекторы
        title_link = first.select_one('a[href*="/smartfony/"]')
        if title_link:
            title = title_link.get_text(strip=True)
            href = title_link.get('href', '')
            print(f"✅ Название: {title}")
            print(f"✅ Ссылка: {href}")
        else:
            print("❌ Название не найдено")
        
        # Тестируем поиск цены
        price_texts = first.find_all(string=lambda text: text and 'р.' in str(text))
        if price_texts:
            price_text = price_texts[0].strip()
            print(f"✅ Цена найдена: {price_text}")
        else:
            print("❌ Цена не найдена")
        
        # Тестируем парсер
        result = parser.parse_product(first)
        if result:
            print(f"✅ Парсер работает!")
            print(f"   Название: {result['title']}")
            print(f"   Цена: {result['price']} руб.")
            print(f"   Ссылка: {result['link'][:50]}...")
        else:
            print("❌ Парсер не работает")

if __name__ == "__main__":
    quick_test_world_devices()



