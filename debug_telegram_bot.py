#!/usr/bin/env python3
"""
Отладка Telegram бота
"""
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные окружения
load_dotenv()

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_telegram_bot():
    """Отладка Telegram бота"""
    print("🔍 Отладка Telegram бота...")
    
    try:
        # Проверяем настройки
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        print(f"Bot Token: {bot_token[:10]}...")
        print(f"Chat ID: {chat_id}")
        
        # Импортируем бота
        from telegram_search_bot import TechSearchBot
        
        print("\n🔍 Создаем экземпляр бота...")
        bot = TechSearchBot()
        print("✅ Бот создан успешно")
        
        # Тестируем поисковую систему
        print("\n🔍 Тестируем поисковую систему...")
        query = "iPhone 15 PRO 512"
        results = bot.search_engine.search_all_stores(query)
        
        print(f"Результаты поиска '{query}':")
        print(f"  Всего найдено: {results['total_found']}")
        print(f"  Топ результатов: {len(results['top_results'])}")
        
        if results['top_results']:
            print("✅ Поиск работает!")
            
            # Тестируем формирование сообщения
            print("\n🔍 Тестируем формирование сообщения...")
            
            response_message = f"""
🔍 **Результаты поиска: {query}**

📊 **Найдено товаров:** {results['total_found']}
⏰ **Время поиска:** {datetime.now().strftime('%H:%M:%S')}

🏆 **Топ {len(results['top_results'])} самых дешевых:**
            """
            
            for i, result in enumerate(results["top_results"], 1):
                response_message += f"""
{i}. **{result['title']}**
💰 **Цена:** {result['price']:,} ₽
🏪 **Магазин:** {result['store']}
🔗 [Перейти к товару]({result['link']})
                """
            
            # Добавляем информацию по магазинам
            response_message += "\n\n📈 **Результаты по магазинам:**\n"
            for store_name, store_results in results["store_results"].items():
                response_message += f"• {store_name}: {len(store_results)} товаров\n"
            
            print(f"Длина сообщения: {len(response_message)} символов")
            print("✅ Сообщение сформировано успешно")
            
            # Проверяем, что сообщение не превышает лимит Telegram
            if len(response_message) <= 4096:
                print("✅ Длина сообщения подходит для Telegram")
            else:
                print("❌ Длина сообщения превышает лимит Telegram")
                return False
                
        else:
            print("❌ Поиск не нашел товары")
            return False
            
        # Тестируем отправку сообщения
        print("\n📤 Тестируем отправку сообщения...")
        
        import requests
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': response_message,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }
        
        response = requests.post(url, data=data, timeout=30)
        
        if response.status_code == 200:
            print("✅ Сообщение успешно отправлено в Telegram!")
            return True
        else:
            print(f"❌ Ошибка отправки в Telegram: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if debug_telegram_bot():
        print("\n🎉 Отладка завершена успешно!")
    else:
        print("\n❌ Отладка провалилась!")
        sys.exit(1)
