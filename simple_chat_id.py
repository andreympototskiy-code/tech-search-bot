#!/usr/bin/env python3
"""
Простой скрипт для получения Chat ID
"""

import asyncio
import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram import Bot
from config.settings import TELEGRAM_BOT_TOKEN

async def get_chat_id():
    """Получение Chat ID"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        updates = await bot.get_updates()
        
        print("🤖 Получение Chat ID")
        print("=" * 30)
        
        if updates:
            print("✅ Найдены сообщения:")
            for update in updates:
                if update.message:
                    chat_id = update.message.chat_id
                    chat_type = update.message.chat.type
                    username = update.message.from_user.username
                    first_name = update.message.from_user.first_name
                    
                    print(f"Chat ID: {chat_id}")
                    print(f"Тип: {chat_type}")
                    print(f"Пользователь: {first_name} (@{username})")
                    print("-" * 20)
                    
                    return chat_id
        else:
            print("❌ Сообщения не найдены")
            print("\n📋 Инструкция:")
            print("1. Найдите вашего бота в Telegram")
            print("2. Напишите боту: /start")
            print("3. Запустите этот скрипт снова")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    asyncio.run(get_chat_id())

