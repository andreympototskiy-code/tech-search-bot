#!/usr/bin/env python3
"""
Скрипт для запуска только Telegram бота (без веб-интерфейса и планировщика)
"""

import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_search_bot import main

if __name__ == '__main__':
    print("🤖 Запуск Telegram бота для поиска техники")
    print("=" * 50)
    print("📱 Бот будет работать только по запросам из Telegram")
    print("🔍 Напишите боту 'что ищем' или описание товара")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("=" * 50)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
