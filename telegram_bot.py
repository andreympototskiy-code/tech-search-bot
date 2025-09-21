import asyncio
from telegram import Bot
from telegram.error import TelegramError
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID
    
    async def send_search_results(self, search_data: dict):
        """Отправка результатов поиска в Telegram"""
        if not self.bot.token or not self.chat_id:
            logger.warning("Telegram настройки не настроены")
            return False
        
        try:
            query = search_data['query']
            top_results = search_data['top_results']
            total_found = search_data['total_found']
            
            message = f"🔍 **Результаты поиска: {query}**\n\n"
            message += f"📊 Найдено товаров: {total_found}\n"
            message += f"🏆 Топ {len(top_results)} самых дешевых:\n\n"
            
            for i, result in enumerate(top_results, 1):
                message += f"{i}. **{result['title']}**\n"
                message += f"💰 Цена: {result['price']:,} ₽\n"
                message += f"🏪 Магазин: {result['store']}\n"
                message += f"🔗 [Ссылка]({result['link']})\n\n"
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            
            logger.info(f"Результаты поиска отправлены в Telegram для запроса: {query}")
            return True
            
        except TelegramError as e:
            logger.error(f"Ошибка отправки в Telegram: {e}")
            return False
        except Exception as e:
            logger.error(f"Неожиданная ошибка при отправке в Telegram: {e}")
            return False
    
    async def send_error_notification(self, error_message: str):
        """Отправка уведомления об ошибке"""
        if not self.bot.token or not self.chat_id:
            return False
        
        try:
            message = f"❌ **Ошибка в системе поиска техники**\n\n{error_message}"
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления об ошибке: {e}")
            return False
    
    def send_search_results_sync(self, search_data: dict):
        """Синхронная версия отправки результатов"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.send_search_results(search_data))
        finally:
            loop.close()
    
    def send_error_notification_sync(self, error_message: str):
        """Синхронная версия отправки уведомления об ошибке"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.send_error_notification(error_message))
        finally:
            loop.close()

