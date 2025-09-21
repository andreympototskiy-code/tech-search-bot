#!/usr/bin/env python3
"""
Скрипт для получения Chat ID из Telegram бота
"""

import asyncio
import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram import Bot
from config.settings import TELEGRAM_BOT_TOKEN

async def get_updates():
    """Получение обновлений от бота для определения Chat ID"""
    print("🤖 Получение Chat ID от Telegram бота")
    print("=" * 40)
    print(f"Токен бота: {TELEGRAM_BOT_TOKEN[:10]}...")
    print()
    print("📋 Инструкция:")
    print("1. Найдите вашего бота в Telegram")
    print("2. Напишите боту любое сообщение (например, /start)")
    print("3. Нажмите Enter для получения Chat ID")
    print()
    
    input("Нажмите Enter после отправки сообщения боту...")
    
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Получаем обновления
        updates = await bot.get_updates()
        
        if updates:
            print("✅ Найдены обновления:")
            print()
            
            for update in updates:
                if update.message:
                    chat_id = update.message.chat_id
                    chat_type = update.message.chat.type
                    username = update.message.from_user.username
                    first_name = update.message.from_user.first_name
                    message_text = update.message.text
                    
                    print(f"Chat ID: {chat_id}")
                    print(f"Тип чата: {chat_type}")
                    print(f"Пользователь: {first_name} (@{username})")
                    print(f"Сообщение: {message_text}")
                    print("-" * 30)
                    
                    # Если это личный чат
                    if chat_type == 'private':
                        print(f"✅ Ваш Chat ID для личного чата: {chat_id}")
                        print("Обновите настройки в config/settings.py")
                    
                    # Если это группа
                    elif chat_type in ['group', 'supergroup']:
                        print(f"✅ Chat ID группы: {chat_id}")
                        print("Обновите настройки в config/settings.py")
                    
        else:
            print("❌ Обновления не найдены")
            print("Убедитесь, что вы написали боту сообщение")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def main():
    print("🚀 Получение Chat ID для Telegram бота")
    print("=" * 50)
    
    # Запускаем асинхронную функцию
    asyncio.run(get_updates())
    
    print("\n📝 После получения Chat ID:")
    print("1. Обновите TELEGRAM_CHAT_ID в config/settings.py")
    print("2. Запустите test_telegram.py для проверки")

if __name__ == '__main__':
    main()

