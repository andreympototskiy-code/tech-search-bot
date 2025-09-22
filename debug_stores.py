#!/usr/bin/env python3
"""
Детальная диагностика магазинов
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
from parsers.world_devices_parser import WorldDevicesParser
from parsers.gsm_store_parser import GSMStoreParser


def debug_store(parser, store_name, test_query="iPhone 15"):
    """Детальная диагностика одного магазина"""
    print(f"\n🔍 Детальная диагностика {store_name}")
    print("=" * 60)

    try:
        # Получаем URL для поиска
        search_url = parser.get_search_url(test_query)
        print(f"URL поиска: {search_url}")

        # Пробуем получить страницу
        print("Попытка получить страницу...")
        response = parser.get_page(search_url)

        if response:
            print(f"✅ Страница получена: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type', 'неизвестно')}")
            print(f"Content-Length: {len(response.text)} символов")

            # Проверяем содержимое
            if "товар" in response.text.lower() or "product" in response.text.lower():
                print("✅ Страница содержит товары")
            else:
                print("❌ Страница не содержит товары")

            # Сохраняем HTML для анализа
            filename = f"debug_{store_name.lower().replace(' ', '_')}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"HTML сохранен в {filename}")

        else:
            print("❌ Не удалось получить страницу")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback

        traceback.print_exc()


def main():
    print("🚀 Детальная диагностика магазинов")
    print("=" * 60)

    # Тестируем каждый магазин
    debug_store(PiterGSMParser(), "PiterGSM")
    time.sleep(5)

    debug_store(WorldDevicesParser(), "World Devices")
    time.sleep(5)

    debug_store(GSMStoreParser(), "GSM Store")

    print("\n" + "=" * 60)
    print("✅ Диагностика завершена")


if __name__ == "__main__":
    main()
