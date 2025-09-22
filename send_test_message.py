#!/usr/bin/env python3
"""
Отправка тестового сообщения боту
"""

import asyncio
import sys
import os
sys.path.append('.')

from telegram import Bot
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

async def send_test_message():
    """Отправка тестового сообщения"""
    try:
        print("📤 Отправка тестового сообщения...")
        
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Отправляем тестовое сообщение
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text="🔍 **Тест бота**\n\nПопробуйте написать боту:\n• /start\n• что ищем\n• iPhone 15 PRO 256gb\n\nБот должен ответить! 🤖",
            parse_mode='Markdown'
        )
        
        print("✅ Тестовое сообщение отправлено!")
        print("💡 Теперь попробуйте написать боту в Telegram")
        
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

if __name__ == "__main__":
    asyncio.run(send_test_message())





