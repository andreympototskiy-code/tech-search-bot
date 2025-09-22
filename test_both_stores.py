#!/usr/bin/env python3
"""
Тестирование обоих рабочих магазинов
"""
import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Устанавливаем тестовые токены
os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
os.environ["TELEGRAM_CHAT_ID"] = "123456789"

from parsers.pitergsm_parser import PiterGSMParser
from parsers.world_devices_parser import WorldDevicesParser


def test_both_stores():
    """Тестируем оба магазина"""
    print("🔍 Тестируем оба рабочих магазина")
    print("=" * 60)

    test_query = "iPhone 15"

    # Тестируем PiterGSM
    print(f"\n1. PiterGSM:")
    pitergsm_parser = PiterGSMParser()
    pitergsm_results = pitergsm_parser.search_products(test_query)
    print(f"   Найдено товаров: {len(pitergsm_results)}")

    if pitergsm_results:
        print("   Первые 2 товара:")
        for i, product in enumerate(pitergsm_results[:2], 1):
            print(f"     {i}. {product['title'][:60]}... - {product['price']} руб.")

    # Тестируем World Devices
    print(f"\n2. World Devices:")
    world_devices_parser = WorldDevicesParser()
    world_devices_results = world_devices_parser.search_products(test_query)
    print(f"   Найдено товаров: {len(world_devices_results)}")

    if world_devices_results:
        print("   Первые 2 товара:")
        for i, product in enumerate(world_devices_results[:2], 1):
            print(f"     {i}. {product['title'][:60]}... - {product['price']} руб.")

    # Итоги
    total_results = len(pitergsm_results) + len(world_devices_results)
    print(f"\n✅ Итого найдено товаров: {total_results}")
    print(f"   - PiterGSM: {len(pitergsm_results)}")
    print(f"   - World Devices: {len(world_devices_results)}")


if __name__ == "__main__":
    test_both_stores()
