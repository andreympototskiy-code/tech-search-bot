#!/usr/bin/env python3
"""
Тест потока сообщений бота
"""

import asyncio
import sys
import os
sys.path.append('.')

from telegram import Bot
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

async def test_message_flow():
    """Тестирование потока сообщений"""
    try:
        print("🧪 Тестирование потока сообщений...")
        
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Отправляем тестовое сообщение
        print("📤 Отправка тестового сообщения...")
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text="🧪 **Тест потока сообщений**\n\nЭто тестовое сообщение для проверки работы бота.\n\nПопробуйте ответить на него!",
            parse_mode='Markdown'
        )
        
        print("✅ Сообщение отправлено!")
        print("⏳ Ожидание ответа...")
        
        # Ждем 10 секунд и проверяем обновления
        await asyncio.sleep(10)
        
        updates = await bot.get_updates()
        print(f"📨 Получено обновлений после теста: {len(updates)}")
        
        if updates:
            print("📝 Последние сообщения:")
            for update in updates[-3:]:
                if update.message:
                    user = update.message.from_user
                    text = update.message.text or "[медиа/стикер]"
                    print(f"  - {user.first_name}: {text}")
        
        print("\n💡 Инструкции для тестирования:")
        print("1. Найдите бота @FindTechPotBot в Telegram")
        print("2. Напишите /start")
        print("3. Напишите 'что ищем'")
        print("4. Отправьте описание товара (например: iPhone 15 PRO 256gb)")
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")

if __name__ == "__main__":
    asyncio.run(test_message_flow())





