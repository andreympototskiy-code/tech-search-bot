#!/usr/bin/env python3
"""
Детальное тестирование парсеров с анализом HTML
"""

import sys
import os
import requests
from bs4 import BeautifulSoup

sys.path.append(".")


def test_store_directly(store_name, url, headers=None):
    """Прямое тестирование магазина"""
    print(f"\n🔍 Тестирование {store_name}")
    print("-" * 50)

    if not headers:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    try:
        print(f"📡 Запрос к: {url}")
        response = requests.get(url, headers=headers, timeout=15)

        print(f"📊 Статус ответа: {response.status_code}")
        print(f"📏 Размер ответа: {len(response.text)} символов")
        print(f"🔗 Финальный URL: {response.url}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")

            # Проверяем заголовок страницы
            title = soup.find("title")
            if title:
                print(f"📄 Заголовок страницы: {title.get_text()[:100]}...")

            # Ищем признаки блокировки
            if any(
                word in response.text.lower()
                for word in ["blocked", "captcha", "robot", "bot"]
            ):
                print("🤖 Обнаружена возможная блокировка ботов")

            # Ищем товары
            product_selectors = [
                ".product-item",
                ".product-layout",
                ".product-card",
                ".catalog-item",
                ".goods-item",
                "[data-product]",
                ".item",
            ]

            products_found = 0
            for selector in product_selectors:
                elements = soup.select(selector)
                if elements:
                    print(
                        f"✅ Найдены элементы с селектором '{selector}': {len(elements)}"
                    )
                    products_found += len(elements)
                else:
                    print(f"❌ Элементы с селектором '{selector}' не найдены")

            if products_found == 0:
                print("❌ Товары не найдены на странице")
                print("🔍 Первые 500 символов HTML:")
                print(response.text[:500])
            else:
                print(f"✅ Всего найдено товаров: {products_found}")

        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            print(f"📄 Первые 200 символов ответа:")
            print(response.text[:200])

    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")


def main():
    """Основная функция тестирования"""
    print("🧪 Детальное тестирование магазинов")
    print("=" * 60)

    # Тестовые URL для каждого магазина
    stores = [
        {
            "name": "PiterGSM",
            "url": "https://pitergsm.ru/?digiSearch=true&term=iPhone%2015%20PRO%20256gb&params=%7Csort%3DDEFAULT",
        },
        {
            "name": "World Devices",
            "url": "https://world-devices.ru/search/?search=iPhone%2015%20PRO%20256gb&description=true",
        },
        {
            "name": "GSM Store",
            "url": "https://gsm-store.ru/?digiSearch=true&term=iPhone%2015%20PRO%20256gb&params=%7Csort%3DDEFAULT",
        },
        {
            "name": "DNS",
            "url": "https://www.dns-shop.ru/search/?q=iPhone%2015%20PRO%20256gb",
        },
        {
            "name": "М.Видео",
            "url": "https://www.mvideo.ru/products/search?q=iPhone%2015%20PRO%20256gb",
        },
        {
            "name": "Эльдорадо",
            "url": "https://www.eldorado.ru/search/?q=iPhone%2015%20PRO%20256gb",
        },
        {
            "name": "Ситилинк",
            "url": "https://www.citilink.ru/search/?text=iPhone%2015%20PRO%20256gb",
        },
    ]

    for store in stores:
        test_store_directly(store["name"], store["url"])


if __name__ == "__main__":
    main()
