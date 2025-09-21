#!/usr/bin/env python3
"""
Основной файл запуска системы поиска техники
"""

import os
import sys
import argparse
import logging
from datetime import datetime

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_interface.app import app
from scheduler import scheduler
from search_engine import SearchEngine
from telegram_bot import TelegramNotifier
from config.settings import WEB_HOST, WEB_PORT, DEBUG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tech_search.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_web_interface():
    """Запуск веб-интерфейса"""
    logger.info("Запуск веб-интерфейса...")
    app.run(host=WEB_HOST, port=WEB_PORT, debug=DEBUG)

def run_scheduler():
    """Запуск планировщика"""
    logger.info("Запуск планировщика...")
    scheduler.start_scheduler()
    
    try:
        # Держим планировщик активным
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Остановка планировщика...")
        scheduler.stop_scheduler()

def run_manual_search(query: str):
    """Ручной запуск поиска"""
    logger.info(f"Ручной поиск: {query}")
    
    try:
        search_engine = SearchEngine()
        telegram_notifier = TelegramNotifier()
        
        results = search_engine.search_all_stores(query)
        telegram_notifier.send_search_results_sync(results)
        
        print(f"\nРезультаты поиска для '{query}':")
        print(f"Найдено товаров: {results['total_found']}")
        print(f"Топ {len(results['top_results'])} самых дешевых:")
        
        for i, result in enumerate(results['top_results'], 1):
            print(f"{i}. {result['title']}")
            print(f"   Цена: {result['price']:,} ₽")
            print(f"   Магазин: {result['store']}")
            print(f"   Ссылка: {result['link']}")
            print()
        
        return results
        
    except Exception as e:
        logger.error(f"Ошибка при ручном поиске: {e}")
        print(f"Ошибка: {e}")
        return None

def add_scheduled_query(query: str):
    """Добавление запроса для регулярного поиска"""
    scheduler.add_scheduled_query(query)
    print(f"Добавлен запрос для регулярного поиска: {query}")

def list_scheduled_queries():
    """Список запланированных запросов"""
    queries = scheduler.get_scheduled_queries()
    if queries:
        print("Запланированные запросы:")
        for i, query in enumerate(queries, 1):
            print(f"{i}. {query}")
    else:
        print("Нет запланированных запросов")

def main():
    parser = argparse.ArgumentParser(description='Система поиска техники')
    parser.add_argument('command', choices=[
        'web', 'scheduler', 'search', 'add-query', 'list-queries', 'telegram-bot'
    ], help='Команда для выполнения')
    parser.add_argument('--query', '-q', help='Запрос для поиска')
    parser.add_argument('--host', default=WEB_HOST, help='Хост для веб-интерфейса')
    parser.add_argument('--port', type=int, default=WEB_PORT, help='Порт для веб-интерфейса')
    
    args = parser.parse_args()
    
    if args.command == 'web':
        run_web_interface()
    elif args.command == 'scheduler':
        run_scheduler()
    elif args.command == 'search':
        if not args.query:
            print("Ошибка: необходимо указать запрос с помощью --query")
            sys.exit(1)
        run_manual_search(args.query)
    elif args.command == 'add-query':
        if not args.query:
            print("Ошибка: необходимо указать запрос с помощью --query")
            sys.exit(1)
        add_scheduled_query(args.query)
    elif args.command == 'list-queries':
        list_scheduled_queries()
    elif args.command == 'telegram-bot':
        from telegram_search_bot import main as telegram_main
        telegram_main()

if __name__ == '__main__':
    main()

