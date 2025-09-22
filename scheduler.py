import schedule
import time
import threading
from datetime import datetime
from search_engine import SearchEngine
from telegram_bot import TelegramNotifier
from config.settings import SEARCH_INTERVAL_HOURS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskScheduler:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.telegram_notifier = TelegramNotifier()
        self.running = False
        self.scheduled_queries = []

    def add_scheduled_query(self, query: str):
        """Добавление запроса для регулярного поиска"""
        if query not in self.scheduled_queries:
            self.scheduled_queries.append(query)
            logger.info(f"Добавлен запрос для регулярного поиска: {query}")

    def remove_scheduled_query(self, query: str):
        """Удаление запроса из регулярного поиска"""
        if query in self.scheduled_queries:
            self.scheduled_queries.remove(query)
            logger.info(f"Удален запрос из регулярного поиска: {query}")

    def get_scheduled_queries(self):
        """Получение списка запланированных запросов"""
        return self.scheduled_queries.copy()

    def perform_scheduled_search(self):
        """Выполнение запланированного поиска"""
        if not self.scheduled_queries:
            logger.info("Нет запланированных запросов для поиска")
            return

        logger.info(
            f"Начинаем запланированный поиск для {len(self.scheduled_queries)} запросов"
        )

        for query in self.scheduled_queries:
            try:
                logger.info(f"Выполняем поиск: {query}")
                results = self.search_engine.search_all_stores(query)

                # Отправляем результаты в Telegram
                self.telegram_notifier.send_search_results_sync(results)

                logger.info(f"Поиск завершен для запроса: {query}")

            except Exception as e:
                error_msg = f"Ошибка при запланированном поиске '{query}': {str(e)}"
                logger.error(error_msg)
                self.telegram_notifier.send_error_notification_sync(error_msg)

    def start_scheduler(self):
        """Запуск планировщика"""
        if self.running:
            logger.warning("Планировщик уже запущен")
            return

        # Настраиваем расписание
        schedule.every(SEARCH_INTERVAL_HOURS).hours.do(self.perform_scheduled_search)

        self.running = True
        logger.info(f"Планировщик запущен. Поиск каждые {SEARCH_INTERVAL_HOURS} часов")

        # Запускаем планировщик в отдельном потоке
        scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        scheduler_thread.start()

        return scheduler_thread

    def stop_scheduler(self):
        """Остановка планировщика"""
        self.running = False
        schedule.clear()
        logger.info("Планировщик остановлен")

    def _run_scheduler(self):
        """Основной цикл планировщика"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Проверяем каждую минуту
            except Exception as e:
                logger.error(f"Ошибка в планировщике: {e}")
                time.sleep(60)

    def run_manual_search(self, query: str):
        """Ручной запуск поиска"""
        try:
            logger.info(f"Ручной поиск: {query}")
            results = self.search_engine.search_all_stores(query)
            self.telegram_notifier.send_search_results_sync(results)
            return results
        except Exception as e:
            error_msg = f"Ошибка при ручном поиске '{query}': {str(e)}"
            logger.error(error_msg)
            self.telegram_notifier.send_error_notification_sync(error_msg)
            raise e


# Глобальный экземпляр планировщика
scheduler = TaskScheduler()
