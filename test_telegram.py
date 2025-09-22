#!/usr/bin/env python3
"""
Скрипт для тестирования Telegram бота
"""

import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import TelegramNotifier

def test_telegram_connection():
    """Тестирование подключения к Telegram"""
    print("🤖 Тестирование Telegram бота")
    print("=" * 40)
    
    try:
        notifier = TelegramNotifier()
        
        print(f"Токен бота: {notifier.bot.token[:10]}...")
        print(f"Chat ID: {notifier.chat_id}")
        
        # Тестовое сообщение
        test_data = {
            'query': 'Тестовый поиск iPhone 15 PRO 256gb',
            'total_found': 5,
            'top_results': [
                {
                    'title': 'iPhone 15 PRO 256gb (тестовый)',
                    'price': 89990,
                    'store': 'Тестовый магазин',
                    'link': 'https://example.com'
                }
            ],
            'search_time': '2024-01-01T12:00:00'
        }
        
        print("\n📤 Отправка тестового сообщения...")
        success = notifier.send_search_results_sync(test_data)
        
        if success:
            print("✅ Тестовое сообщение отправлено успешно!")
            print("📱 Проверьте ваш Telegram чат")
        else:
            print("❌ Ошибка отправки сообщения")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def send_test_message():
    """Отправка простого тестового сообщения"""
    print("\n📤 Отправка простого тестового сообщения...")
    
    try:
        notifier = TelegramNotifier()
        error_message = "🧪 Это тестовое сообщение от системы поиска техники!"
        
        success = notifier.send_error_notification_sync(error_message)
        
        if success:
            print("✅ Простое сообщение отправлено!")
        else:
            print("❌ Ошибка отправки простого сообщения")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    print("🚀 Тестирование Telegram интеграции")
    print("=" * 50)
    
    # Тестируем подключение
    test_telegram_connection()
    
    # Отправляем простое сообщение
    send_test_message()
    
    print("\n✨ Тестирование завершено!")
    print("\nЕсли сообщения не пришли:")
    print("1. Проверьте правильность токена бота")
    print("2. Убедитесь, что вы написали боту хотя бы одно сообщение")
    print("3. Проверьте правильность Chat ID")






