#!/usr/bin/env python3
"""
Детальная диагностика PiterGSM
"""
import os
import sys
import time
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Устанавливаем тестовые токены
os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
os.environ["TELEGRAM_CHAT_ID"] = "123456789"

from parsers.pitergsm_parser import PiterGSMParser
import requests
import brotli


def debug_pitergsm():
    """Детальная диагностика PiterGSM"""
    print("🔍 Детальная диагностика PiterGSM")
    print("=" * 60)

    parser = PiterGSMParser()
    test_query = "iPhone 15"
    search_url = parser.get_search_url(test_query)

    print(f"URL поиска: {search_url}")

    # Пробуем получить страницу напрямую
    print("\n1. Прямой запрос через requests:")
    try:
        response = requests.get(search_url, headers=parser.session.headers, timeout=15)
        print(f"Статус: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Content-Encoding: {response.headers.get('content-encoding')}")
        print(f"Content-Length: {len(response.content)} байт")

        # Проверяем, сжато ли содержимое
        if response.headers.get("content-encoding") == "br":
            print("Содержимое сжато Brotli")
            try:
                decompressed = brotli.decompress(response.content)
                print(f"После декомпрессии: {len(decompressed)} байт")

                # Сохраняем декомпрессированное содержимое
                with open("pitergsm_decompressed.html", "w", encoding="utf-8") as f:
                    f.write(decompressed.decode("utf-8"))
                print(
                    "Декомпрессированное содержимое сохранено в pitergsm_decompressed.html"
                )

                # Проверяем, есть ли товары
                if (
                    "товар" in decompressed.decode("utf-8").lower()
                    or "product" in decompressed.decode("utf-8").lower()
                ):
                    print("✅ Декомпрессированное содержимое содержит товары")
                else:
                    print("❌ Декомпрессированное содержимое не содержит товары")

            except Exception as e:
                print(f"❌ Ошибка декомпрессии: {e}")
        else:
            print("Содержимое не сжато")

    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

    # Пробуем через парсер
    print("\n2. Через парсер:")
    try:
        results = parser.search_products(test_query)
        print(f"Найдено товаров: {len(results)}")

        if results:
            print("Первые 3 товара:")
            for i, product in enumerate(results[:3], 1):
                print(f"  {i}. {product['title']} - {product['price']} руб.")
        else:
            print("Товары не найдены")

    except Exception as e:
        print(f"❌ Ошибка парсера: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    debug_pitergsm()
