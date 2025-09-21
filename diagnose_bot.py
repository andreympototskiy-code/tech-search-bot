#!/usr/bin/env python3
"""
Диагностика состояния бота
"""

import sys
import os
import subprocess
sys.path.append('.')

def check_bot_status():
    """Проверка статуса бота"""
    print("🔍 Диагностика состояния Telegram бота...")
    print("=" * 50)
    
    # 1. Проверяем, запущен ли бот
    print("1️⃣ Проверка запущенных процессов...")
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        bot_processes = [line for line in result.stdout.split('\n') if 'telegram_search_bot' in line and 'python' in line]
        
        if bot_processes:
            print(f"✅ Бот запущен ({len(bot_processes)} процессов)")
            for proc in bot_processes:
                parts = proc.split()
                if len(parts) > 1:
                    pid = parts[1]
                    print(f"   PID: {pid}")
        else:
            print("❌ Бот не запущен")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки процессов: {e}")
    
    # 2. Проверяем .env файл
    print("\n2️⃣ Проверка конфигурации...")
    env_path = '.env'
    if os.path.exists(env_path):
        print("✅ Файл .env найден")
        with open(env_path, 'r') as f:
            content = f.read()
            if 'TELEGRAM_BOT_TOKEN' in content and 'TELEGRAM_CHAT_ID' in content:
                print("✅ Токены настроены")
            else:
                print("❌ Токены не настроены")
                return False
    else:
        print("❌ Файл .env не найден")
        return False
    
    # 3. Проверяем зависимости
    print("\n3️⃣ Проверка зависимостей...")
    try:
        import telegram
        print("✅ python-telegram-bot установлен")
    except ImportError:
        print("❌ python-telegram-bot не установлен")
        return False
    
    # 4. Проверяем виртуальное окружение
    print("\n4️⃣ Проверка виртуального окружения...")
    if os.path.exists('venv/bin/activate'):
        print("✅ Виртуальное окружение найдено")
    else:
        print("❌ Виртуальное окружение не найдено")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Все проверки пройдены успешно!")
    print("\n💡 Рекомендации:")
    print("1. Убедитесь, что бот запущен: ./run_bot.sh")
    print("2. Напишите боту в Telegram: /start")
    print("3. Попробуйте: что ищем")
    print("4. Затем отправьте: iPhone 15 PRO 256gb")
    
    return True

if __name__ == "__main__":
    check_bot_status()
