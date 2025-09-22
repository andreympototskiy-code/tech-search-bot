#!/usr/bin/env python3
"""
Детальная отладка парсеров PiterGSM и World Devices
"""

import sys
import os
sys.path.append('.')

from parsers.pitergsm_parser import PiterGSMParser
from parsers.world_devices_parser import WorldDevicesParser
import requests
from bs4 import BeautifulSoup

def debug_world_devices():
    """Отладка World Devices"""
    print("🔍 Отладка World Devices")
    print("=" * 50)
    
    parser = WorldDevicesParser()
    query = "iPhone 15 PRO 256gb"
    search_url = f"https://world-devices.ru/search/?search={query}&description=true"
    
    response = parser.get_page(search_url)
    if not response:
        print("❌ Не удалось получить страницу")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем элементы товаров
    product_elements = soup.select('.product-layout')
    print(f"📦 Найдено .product-layout: {len(product_elements)}")
    
    if product_elements:
        first_product = product_elements[0]
        
        print(f"\n🔍 Анализ первого товара:")
        print(f"HTML структура: {str(first_product)[:300]}...")
        
        # Ищем все ссылки
        links = first_product.find_all('a')
        print(f"\n🔗 Найдено ссылок: {len(links)}")
        for i, link in enumerate(links):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            print(f"  {i+1}. href='{href}' text='{text[:40]}...'")
        
        # Ищем заголовки
        headers = first_product.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        print(f"\n📝 Найдено заголовков: {len(headers)}")
        for i, header in enumerate(headers):
            text = header.get_text(strip=True)
            print(f"  {i+1}. <{header.name}> {text}")
        
        # Ищем цены
        price_texts = first_product.find_all(text=lambda text: text and ('р.' in str(text) or 'руб' in str(text)))
        print(f"\n💰 Найдено цен: {len(price_texts)}")
        for i, price in enumerate(price_texts):
            print(f"  {i+1}. {price}")

def debug_pitergsm():
    """Отладка PiterGSM"""
    print("\n🔍 Отладка PiterGSM")
    print("=" * 50)
    
    parser = PiterGSMParser()
    query = "iPhone 15 PRO 256gb"
    search_url = f"https://pitergsm.ru/?digiSearch=true&term={query}&params=%7Csort%3DDEFAULT"
    
    response = parser.get_page(search_url)
    if not response:
        print("❌ Не удалось получить страницу")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Проверяем, что получили
    print(f"📄 Размер HTML: {len(response.text)} символов")
    print(f"📄 Заголовок страницы: {soup.find('title').get_text() if soup.find('title') else 'Не найден'}")
    
    # Ищем элементы товаров
    product_selectors = [
        '.product-item',
        '.product-card',
        '.product-layout',
        '.item',
        '[data-product]',
        '.goods-item'
    ]
    
    for selector in product_selectors:
        elements = soup.select(selector)
        print(f"📦 Найдено '{selector}': {len(elements)}")
        if elements and len(elements) > 0:
            print(f"  Первый элемент: {str(elements[0])[:200]}...")
    
    # Ищем любые div с классами
    all_divs = soup.find_all('div', class_=True)
    print(f"\n🔍 Всего div с классами: {len(all_divs)}")
    
    # Группируем по классам
    class_counts = {}
    for div in all_divs:
        for cls in div.get('class', []):
            class_counts[cls] = class_counts.get(cls, 0) + 1
    
    # Показываем самые частые классы
    sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
    print("📊 Топ-10 классов div:")
    for cls, count in sorted_classes[:10]:
        print(f"  {cls}: {count}")

def main():
    """Основная функция"""
    debug_world_devices()
    debug_pitergsm()

if __name__ == "__main__":
    main()



