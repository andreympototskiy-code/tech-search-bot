#!/usr/bin/env python3
"""
Простой тест парсеров
"""
import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Устанавливаем тестовые токены
os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token'
os.environ['TELEGRAM_CHAT_ID'] = '123456789'

from parsers.world_devices_parser import WorldDevicesParser

def test_world_devices():
    """Тестируем World Devices"""
    print("🔍 Тестируем World Devices...")
    
    parser = WorldDevicesParser()
    
    # Тестируем поиск
    results = parser.search_products("iPhone 15")
    
    print(f"Найдено товаров: {len(results)}")
    
    if results:
        print("Первые 3 товара:")
        for i, product in enumerate(results[:3], 1):
            print(f"  {i}. {product['title']} - {product['price']} руб.")
            print(f"     Ссылка: {product['link']}")
    else:
        print("Товары не найдены")

if __name__ == "__main__":
    test_world_devices()
