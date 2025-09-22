#!/usr/bin/env python3
"""
Тестирование отправки уведомлений в Telegram
"""
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные окружения
load_dotenv()

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_telegram_notification():
    """Тестирует отправку уведомления в Telegram"""
    print("🔍 Тестируем отправку уведомления в Telegram...")
    
    try:
        # Проверяем настройки Telegram
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            print("❌ TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не установлены в .env файле")
            return False
            
        print(f"✅ Bot Token: {bot_token[:10]}...")
        print(f"✅ Chat ID: {chat_id}")
        
        # Импортируем и тестируем поисковую систему
        from search_engine import SearchEngine
        
        print("\n🔍 Тестируем поисковую систему...")
        engine = SearchEngine()
        
        # Тестируем поиск iPhone 15 PRO 512
        query = "iPhone 15 PRO 512"
        results = engine.search_all_stores(query)
        
        print(f"Результаты поиска '{query}':")
        print(f"  Всего найдено: {results['total_found']}")
        print(f"  Топ результатов: {len(results['top_results'])}")
        
        if results['top_results']:
            print("✅ Поиск работает корректно!")
            
            # Формируем сообщение для Telegram
            message = f"""🔍 **Проверка системы поиска**

**Запрос:** {query}
**Время:** {datetime.now().strftime('%H:%M:%S')}

📊 **Найдено товаров:** {results['total_found']}
🏆 **Топ результатов:** {len(results['top_results'])}

**Лучшие предложения:**
"""
            
            for i, product in enumerate(results['top_results'][:3], 1):
                message += f"""
{i}. **{product['title'][:50]}...**
💰 **Цена:** {product['price']:,} ₽
🏪 **Магазин:** {product['store']}
"""
            
            message += f"""

✅ **Система работает корректно!**
Все магазины доступны и возвращают результаты.
"""
            
            print(f"Длина сообщения: {len(message)} символов")
            
            # Отправляем уведомление в Telegram
            print("\n📤 Отправляем уведомление в Telegram...")
            
            import requests
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                print("✅ Уведомление успешно отправлено в Telegram!")
                return True
            else:
                print(f"❌ Ошибка отправки в Telegram: {response.status_code}")
                print(f"Ответ: {response.text}")
                return False
                
        else:
            print("❌ Поиск не нашел товары")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_telegram_notification():
        print("\n🎉 Тест завершен успешно!")
    else:
        print("\n❌ Тест провалился!")
        sys.exit(1)
