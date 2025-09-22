#!/usr/bin/env python3
"""
Тестовый скрипт для проверки новых магазинов
"""

import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parsers.world_devices_parser import WorldDevicesParser
from parsers.gsm_store_parser import GSMStoreParser
from parsers.pitergsm_parser import PiterGSMParser


def test_parser(parser, parser_name, test_query):
    """Тестирование парсера"""
    print(f"\n🔍 Тестирование {parser_name}")
    print("=" * 50)
    print(f"Запрос: {test_query}")
    print("-" * 30)

    try:
        results = parser.search_products(test_query)

        if results:
            print(f"✅ Найдено товаров: {len(results)}")
            print()

            for i, result in enumerate(results[:3], 1):
                print(f"{i}. {result['title']}")
                print(f"   💰 Цена: {result['price']:,} ₽")
                print(f"   🏪 Магазин: {result['store']}")
                print(f"   🔗 Ссылка: {result['link']}")
                print()
        else:
            print("❌ Товары не найдены")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

    return len(results) if "results" in locals() else 0


def main():
    print("🧪 Тестирование новых магазинов")
    print("=" * 50)

    # Тестовый запрос
    test_query = "iPhone 15 PRO 256gb"

    # Инициализация парсеров
    parsers = [
        (WorldDevicesParser(), "World Devices"),
        (GSMStoreParser(), "GSM Store"),
        (PiterGSMParser(), "PiterGSM (обновленный)"),
    ]

    total_results = 0

    for parser, name in parsers:
        results_count = test_parser(parser, name, test_query)
        total_results += results_count

    print("\n📊 Итоговая статистика:")
    print(f"Всего найдено товаров: {total_results}")

    if total_results > 0:
        print("✅ Тестирование прошло успешно!")
    else:
        print("⚠️  Возможно, требуется настройка парсеров под текущую структуру сайтов")


if __name__ == "__main__":
    main()
