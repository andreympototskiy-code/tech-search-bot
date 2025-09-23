#!/usr/bin/env python3
"""
Демонстрационный скрипт для тестирования системы поиска техники
"""

import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from search_engine import SearchEngine
from telegram_bot import TelegramNotifier


def demo_search():
    """Демонстрация поиска"""
    print("🔍 Демонстрация системы поиска техники")
    print("=" * 50)

    # Инициализация компонентов
    search_engine = SearchEngine()
    telegram_notifier = TelegramNotifier()

    # Тестовый запрос
    test_query = "iPhone 15 PRO 256gb"

    print(f"Поиск: {test_query}")
    print("-" * 30)

    try:
        # Выполняем поиск
        results = search_engine.search_all_stores(test_query)

        # Выводим результаты
        print(f"✅ Поиск завершен!")
        print(f"📊 Найдено товаров: {results['total_found']}")
        print(f"⏰ Время поиска: {results['search_time']}")
        print()

        if results["top_results"]:
            print("🏆 Топ самых дешевых товаров:")
            for i, result in enumerate(results["top_results"], 1):
                print(f"{i}. {result['title']}")
                print(f"   💰 Цена: {result['price']:,} ₽")
                print(f"   🏪 Магазин: {result['store']}")
                print(f"   🔗 Ссылка: {result['link']}")
                print()

        # Показываем результаты по магазинам
        print("📈 Результаты по магазинам:")
        for store_name, store_results in results["store_results"].items():
            print(f"  {store_name}: {len(store_results)} товаров")

        # Проверяем настройки Telegram
        if telegram_notifier.bot.token and telegram_notifier.chat_id:
            print("\n📱 Отправка результатов в Telegram...")
            success = telegram_notifier.send_search_results_sync(results)
            if success:
                print("✅ Результаты отправлены в Telegram")
            else:
                print("❌ Ошибка отправки в Telegram")
        else:
            print("\n⚠️  Telegram не настроен (отсутствует токен или chat_id)")

        return results

    except Exception as e:
        print(f"❌ Ошибка при поиске: {e}")
        return None


def demo_history():
    """Демонстрация истории поисков"""
    print("\n📚 История поисков:")
    print("-" * 30)

    try:
        search_engine = SearchEngine()
        history = search_engine.get_search_history(5)

        if history:
            for search in history:
                print(f"🔍 {search['query']}")
                print(f"   📅 {search['created_at']}")
                print(f"   📦 {search['results_count']} товаров")
                print()
        else:
            print("История поисков пуста")

    except Exception as e:
        print(f"❌ Ошибка при получении истории: {e}")


if __name__ == "__main__":
    print("🚀 Запуск демонстрации системы поиска техники")
    print()

    # Демонстрация поиска
    results = demo_search()

    # Демонстрация истории
    demo_history()

    print("\n✨ Демонстрация завершена!")
    print("\nДля запуска веб-интерфейса используйте:")
    print("python main.py web")
    print("\nДля ручного поиска используйте:")
    print("python main.py search --query 'ваш запрос'")


