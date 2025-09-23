#!/usr/bin/env python3
"""
Тест Telegram бота для поиска
"""
import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Устанавливаем тестовые токены если не установлены
if not os.getenv('TELEGRAM_BOT_TOKEN'):
    os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token'
if not os.getenv('TELEGRAM_CHAT_ID'):
    os.environ['TELEGRAM_CHAT_ID'] = '123456789'

from telegram_search_bot import TechSearchBot
from search_engine import SearchEngine

def test_search_functionality():
    """Тестируем функциональность поиска"""
    print("🔍 Тестируем функциональность поиска...")
    
    try:
        # Тест 1: Поисковая система
        print("\n1. Тестируем поисковую систему...")
        engine = SearchEngine()
        results = engine.search_all_stores("iPhone 15 pro 256")
        
        print(f"✅ Поисковая система работает")
        print(f"   Найдено товаров: {results['total_found']}")
        print(f"   Топ результатов: {len(results['top_results'])}")
        
        # Тест 2: Telegram бот (без запуска)
        print("\n2. Тестируем инициализацию Telegram бота...")
        bot = TechSearchBot()
        print("✅ Telegram бот инициализирован")
        
        # Тест 3: Формирование сообщения с результатами
        print("\n3. Тестируем формирование сообщения...")
        if results["top_results"]:
            response_message = f"""
🔍 **Результаты поиска: iPhone 15 pro 256**

📊 **Найдено товаров:** {results['total_found']}

🏆 **Топ {len(results['top_results'])} самых дешевых:**
            """
            
            for i, result in enumerate(results["top_results"], 1):
                response_message += f"""
{i}. **{result['title']}**
💰 **Цена:** {result['price']:,} ₽
🏪 **Магазин:** {result['store']}
🔗 [Перейти к товару]({result['link']})
                """
            
            print("✅ Сообщение сформировано успешно")
            print(f"   Длина сообщения: {len(response_message)} символов")
            
            # Проверяем, не слишком ли длинное сообщение для Telegram
            if len(response_message) > 4096:
                print("⚠️  Предупреждение: Сообщение может быть слишком длинным для Telegram")
            else:
                print("✅ Длина сообщения подходит для Telegram")
        
        print("\n🎉 Все тесты прошли успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_search_functionality()
    sys.exit(0 if success else 1)


