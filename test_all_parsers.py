#!/usr/bin/env python3
"""
Тестирование всех парсеров магазинов
"""

import sys
import os
import time
sys.path.append('.')

from parsers.pitergsm_parser import PiterGSMParser
from parsers.world_devices_parser import WorldDevicesParser
from parsers.gsm_store_parser import GSMStoreParser
from parsers.dns_parser import DNSParser
from parsers.mvideo_parser import MVideoParser
from parsers.eldorado_parser import EldoradoParser
from parsers.citilink_parser import CitilinkParser

def test_parser(parser_class, parser_name, test_query="iPhone 15 PRO 256gb"):
    """Тестирование одного парсера"""
    print(f"\n🔍 Тестирование {parser_name}...")
    print("-" * 50)
    
    try:
        # Создаем экземпляр парсера
        parser = parser_class()
        print(f"✅ Парсер {parser_name} инициализирован")
        
        # Тестируем поиск
        print(f"🔎 Поиск по запросу: '{test_query}'")
        start_time = time.time()
        
        results = parser.search_products(test_query)
        
        end_time = time.time()
        search_time = end_time - start_time
        
        print(f"⏱️ Время поиска: {search_time:.2f} секунд")
        print(f"📊 Найдено товаров: {len(results)}")
        
        if results:
            print("📦 Примеры товаров:")
            for i, product in enumerate(results[:3]):  # Показываем первые 3
                print(f"  {i+1}. {product.get('title', 'N/A')[:50]}...")
                print(f"     💰 Цена: {product.get('price', 'N/A')} руб.")
                print(f"     🏪 Магазин: {product.get('store', 'N/A')}")
                print(f"     🔗 Ссылка: {product.get('link', 'N/A')[:50]}...")
                print()
        else:
            print("❌ Товары не найдены")
            
        return {
            'name': parser_name,
            'status': 'success',
            'results_count': len(results),
            'search_time': search_time,
            'results': results[:3] if results else []
        }
        
    except Exception as e:
        print(f"❌ Ошибка в парсере {parser_name}: {e}")
        return {
            'name': parser_name,
            'status': 'error',
            'error': str(e),
            'results_count': 0,
            'search_time': 0
        }

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование всех парсеров магазинов")
    print("=" * 60)
    
    # Список парсеров для тестирования
    parsers_to_test = [
        (PiterGSMParser, "PiterGSM"),
        (WorldDevicesParser, "World Devices"),
        (GSMStoreParser, "GSM Store"),
        (DNSParser, "DNS"),
        (MVideoParser, "М.Видео"),
        (EldoradoParser, "Эльдорадо"),
        (CitilinkParser, "Ситилинк")
    ]
    
    test_query = "iPhone 15 PRO 256gb"
    print(f"🔍 Тестовый запрос: '{test_query}'")
    
    results = []
    
    for parser_class, parser_name in parsers_to_test:
        result = test_parser(parser_class, parser_name, test_query)
        results.append(result)
        
        # Пауза между тестами
        time.sleep(2)
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    
    working_parsers = []
    broken_parsers = []
    
    for result in results:
        if result['status'] == 'success':
            working_parsers.append(result)
            print(f"✅ {result['name']}: {result['results_count']} товаров ({result['search_time']:.1f}с)")
        else:
            broken_parsers.append(result)
            print(f"❌ {result['name']}: ОШИБКА - {result['error']}")
    
    print(f"\n📈 Статистика:")
    print(f"✅ Работающих парсеров: {len(working_parsers)}")
    print(f"❌ Сломанных парсеров: {len(broken_parsers)}")
    
    if broken_parsers:
        print(f"\n🔧 Парсеры, требующие исправления:")
        for parser in broken_parsers:
            print(f"  - {parser['name']}: {parser['error']}")
    
    if working_parsers:
        print(f"\n🏆 Лучшие парсеры по количеству результатов:")
        sorted_parsers = sorted(working_parsers, key=lambda x: x['results_count'], reverse=True)
        for parser in sorted_parsers[:3]:
            print(f"  {parser['name']}: {parser['results_count']} товаров")

if __name__ == "__main__":
    main()

