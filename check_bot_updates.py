#!/usr/bin/env python3
"""
Проверка обновлений от бота
"""

import asyncio
import sys
import os

sys.path.append(".")

from telegram import Bot
from config.settings import TELEGRAM_BOT_TOKEN


async def check_updates():
    """Проверка обновлений"""
    try:
        print("🔍 Проверка обновлений от бота...")

        bot = Bot(token=TELEGRAM_BOT_TOKEN)

        # Получаем обновления
        updates = await bot.get_updates()

        print(f"📨 Получено обновлений: {len(updates)}")

        if updates:
            print("\n📝 Последние сообщения:")
            for i, update in enumerate(updates[-5:]):  # Последние 5
                if update.message:
                    user = update.message.from_user
                    text = update.message.text or "[медиа/стикер]"
                    print(f"  {i+1}. {user.first_name} (@{user.username}): {text}")
        else:
            print("📭 Нет новых сообщений")
            print("💡 Попробуйте написать боту в Telegram")

    except Exception as e:
        print(f"❌ Ошибка получения обновлений: {e}")


if __name__ == "__main__":
    asyncio.run(check_updates())
