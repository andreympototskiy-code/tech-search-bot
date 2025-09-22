#!/usr/bin/env python3
"""
Тестирование доступности магазинов
"""
import os
import sys
import time
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Устанавливаем тестовые токены для избежания ошибок
os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token'
os.environ['TELEGRAM_CHAT_ID'] = '123456789'

from parsers.pitergsm_parser import PiterGSMParser
from parsers.world_devices_parser import WorldDevicesParser
from parsers.gsm_store_parser import GSMStoreParser

def test_store(parser, store_name, test_query="iPhone 15"):
    """Тестирует один магазин"""
    print(f"\n🔍 Тестируем {store_name}...")
    print(f"Запрос: {test_query}")
    
    try:
        # Тестируем поиск
        results = parser.search_products(test_query)
        
        if results:
            print(f"✅ {store_name}: Найдено {len(results)} товаров")
            for i, product in enumerate(results[:3], 1):
                print(f"  {i}. {product['title'][:50]}... - {product['price']} руб.")
        else:
            print(f"❌ {store_name}: Товары не найдены")
            
    except Exception as e:
        print(f"❌ {store_name}: Ошибка - {e}")

def main():
    print("🚀 Тестирование доступности магазинов")
    print("=" * 50)
    
    # Тестируем каждый магазин
    test_store(PiterGSMParser(), "PiterGSM")
    time.sleep(5)  # Пауза между тестами
    
    test_store(WorldDevicesParser(), "World Devices")
    time.sleep(5)
    
    test_store(GSMStoreParser(), "GSM Store")
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено")

if __name__ == "__main__":
    main()

