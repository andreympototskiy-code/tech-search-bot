#!/usr/bin/env python3
"""
Простой тест для CI/CD
"""
import os
import sys

# Устанавливаем тестовые переменные окружения
os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token'
os.environ['TELEGRAM_CHAT_ID'] = '123456789'

try:
    print("Тестируем импорты...")
    
    # Тест 1: Импорт настроек
    import config.settings
    print("✅ Settings imported successfully")
    
    # Тест 2: Импорт парсеров
    from parsers.pitergsm_parser import PiterGSMParser
    from parsers.world_devices_parser import WorldDevicesParser
    print("✅ Parsers imported successfully")
    
    # Тест 3: Инициализация парсеров
    pitergsm = PiterGSMParser()
    world_devices = WorldDevicesParser()
    print("✅ Parsers initialized successfully")
    
    # Тест 4: Импорт поисковой системы
    from search_engine import SearchEngine
    engine = SearchEngine()
    print("✅ Search engine imported and initialized successfully")
    
    # Тест 5: Импорт Telegram бота
    from telegram_search_bot import TechSearchBot
    print("✅ Telegram bot imported successfully")
    
    print("\n🎉 Все тесты прошли успешно!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
