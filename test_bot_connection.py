#!/usr/bin/env python3
"""
Тест подключения к Telegram боту
"""

import asyncio
import sys
import os
sys.path.append('.')

from telegram import Bot
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

async def test_bot_connection():
    """Тестирование подключения к боту"""
    try:
        print("🔍 Тестирование подключения к Telegram боту...")
        print(f"🔑 Токен: {TELEGRAM_BOT_TOKEN[:20]}...")
        print(f"💬 Chat ID: {TELEGRAM_CHAT_ID}")
        
        # Создаем бота
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        print(f"🤖 Бот: @{bot_info.username} ({bot_info.first_name})")
        
        # Проверяем, может ли бот отправлять сообщения
        try:
            await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text="🔍 **Тест подключения**\n\nБот работает корректно! ✅",
                parse_mode='Markdown'
            )
            print("✅ Сообщение отправлено успешно!")
        except Exception as e:
            print(f"❌ Ошибка отправки сообщения: {e}")
            
        # Получаем обновления
        updates = await bot.get_updates()
        print(f"📨 Получено обновлений: {len(updates)}")
        
        if updates:
            print("📝 Последние сообщения:")
            for update in updates[-3:]:  # Последние 3
                if update.message:
                    print(f"  - {update.message.from_user.first_name}: {update.message.text}")
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Запуск теста подключения к Telegram боту...")
    result = asyncio.run(test_bot_connection())
    
    if result:
        print("\n✅ Бот работает корректно!")
        print("💡 Попробуйте написать боту в Telegram:")
        print("   - /start")
        print("   - что ищем")
        print("   - iPhone 15 PRO 256gb")
    else:
        print("\n❌ Проблема с подключением к боту")
