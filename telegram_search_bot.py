#!/usr/bin/env python3
"""
Telegram бот для приема запросов на поиск техники
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from search_engine import SearchEngine
from config.settings import TELEGRAM_BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class TechSearchBot:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.bot_token = TELEGRAM_BOT_TOKEN
        # Словарь для хранения состояния пользователей (ожидание описания товара)
        self.user_states = {}

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_message = """
🔍 **Поиск техники**

Привет! Я помогу найти технику по лучшим ценам.

📝 **Как пользоваться:**
1. Напишите `что ищем` или `поиск товара`
2. Я попрошу описать товар
3. Отправьте описание товара
4. Получите результаты поиска

**Примеры запросов:**
• iPhone 15 PRO 256gb
• Dyson Complete Long
• MacBook Air M2 256gb
• PlayStation 5
• Samsung Galaxy S24

🔍 **Магазины:**
• PiterGSM
• World Devices  
• GSM Store
• DNS
• М.Видео
• Эльдорадо
• Ситилинк

**Команды:**
/help - Подробная справка
/history - История поисков
/cancel - Отменить поиск

Начните с `что ищем`! 🚀
        """

        await update.message.reply_text(welcome_message, parse_mode="Markdown")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_message = """
📖 **Помощь по использованию**

🔍 **Как начать поиск:**
1. Напишите `что ищем` или `поиск товара`
2. Бот попросит описать товар
3. Отправьте описание товара
4. Получите результаты поиска

**Примеры запросов:**
• `iPhone 15 PRO 256gb`
• `Dyson Complete Long`
• `MacBook Air M2`
• `PlayStation 5`

📊 **Что вы получите:**
• Топ-3 самых дешевых варианта
• Цены и ссылки на товары
• Информацию о магазинах

⚙️ **Команды:**
/start - Начать работу
/help - Показать эту справку
/history - История поисков
/cancel - Отменить текущий поиск

💡 **Советы:**
• Указывайте модель и характеристики
• Используйте простые названия
• Проверяйте правильность написания
        """

        await update.message.reply_text(help_message, parse_mode="Markdown")

    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /history"""
        try:
            history = self.search_engine.get_search_history(5)

            if history:
                message = "📚 **Последние поиски:**\n\n"

                for search in history:
                    message += f"🔍 **{search['query']}**\n"
                    message += f"📅 {search['created_at']}\n"
                    message += f"📦 {search['results_count']} товаров\n\n"

                await update.message.reply_text(message, parse_mode="Markdown")
            else:
                await update.message.reply_text("📚 История поисков пуста")

        except Exception as e:
            logger.error(f"Ошибка получения истории: {e}")
            await update.message.reply_text("❌ Ошибка получения истории")

    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /cancel"""
        user_id = update.effective_user.id

        # Сбрасываем состояние пользователя
        if user_id in self.user_states:
            del self.user_states[user_id]

        await update.message.reply_text(
            "❌ **Поиск отменен**\n\n"
            "Состояние сброшено. Вы можете начать новый поиск.",
            parse_mode="Markdown",
        )

    async def handle_search_request(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, query_text=None
    ):
        """Обработчик запросов на поиск"""
        user_message = query_text or update.message.text.strip()
        user_name = update.message.from_user.first_name or "Пользователь"

        logger.info(f"Получен запрос от {user_name}: {user_message}")

        # Отправляем сообщение о начале поиска
        searching_message = f"""
🔍 **Начинаем поиск...**

**Запрос:** {user_message}

⏳ Ищу товары в магазинах...
Это может занять несколько минут.
        """

        status_message = await update.message.reply_text(
            searching_message, parse_mode="Markdown"
        )

        try:
            # Выполняем поиск
            results = self.search_engine.search_all_stores(user_message)

            # Формируем ответ с результатами
            if results["top_results"]:
                response_message = f"""
🔍 **Результаты поиска: {user_message}**

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
                    response_message += (
                        f"• {store_name}: {len(store_results)} товаров\n"
                    )

                # Отправляем результаты
                await status_message.edit_text(
                    response_message,
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                )

            else:
                no_results_message = f"""
❌ **Товары не найдены**

**Запрос:** {user_message}

Возможные причины:
• Товар действительно не найден
• Некоторые магазины временно недоступны
• Попробуйте изменить запрос

💡 **Советы:**
• Используйте более простые названия
• Проверьте правильность написания
• Попробуйте синонимы
                """

                await status_message.edit_text(
                    no_results_message, parse_mode="Markdown"
                )

        except Exception as e:
            logger.error(f"Ошибка при поиске: {e}")
            error_message = f"""
❌ **Ошибка при поиске**

**Запрос:** {user_message}

Произошла ошибка: {str(e)}

Попробуйте еще раз или обратитесь к администратору.
            """

            await status_message.edit_text(error_message, parse_mode="Markdown")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик всех сообщений"""
        user_id = update.effective_user.id
        user_message = update.message.text.strip()
        user_message_lower = user_message.lower()

        # Проверяем, ожидает ли пользователь описания товара
        if (
            user_id in self.user_states
            and self.user_states[user_id] == "waiting_for_product"
        ):
            # Если пользователь написал /cancel, отменяем поиск
            if user_message_lower == "/cancel":
                del self.user_states[user_id]
                await update.message.reply_text(
                    "❌ **Поиск отменен**\n\n"
                    "Состояние сброшено. Вы можете начать новый поиск.",
                    parse_mode="Markdown",
                )
                return

            # Пользователь отправляет описание товара
            self.user_states[user_id] = None  # Сбрасываем состояние
            await self.handle_search_request(update, context, user_message)
            return

        # Проверяем триггеры для начала поиска
        search_triggers = [
            "что ищем",
            "ищем",
            "найти",
            "поиск",
            "найди",
            "поиск товара",
        ]

        if any(trigger in user_message_lower for trigger in search_triggers):
            if user_message_lower in ["что ищем", "поиск товара"]:
                # Запрашиваем описание товара
                self.user_states[user_id] = "waiting_for_product"
                await update.message.reply_text(
                    "📝 **Опишите товар, который хотите найти**\n\n"
                    "**Примеры запросов:**\n"
                    "• iPhone 15 PRO 256gb\n"
                    "• Dyson Complete Long\n"
                    "• MacBook Air M2 256gb\n"
                    "• PlayStation 5\n"
                    "• Samsung Galaxy S24\n"
                    "• AirPods Pro 2\n\n"
                    "💡 **Советы:**\n"
                    "• Указывайте модель и характеристики\n"
                    "• Используйте простые названия\n"
                    "• Проверяйте правильность написания",
                    parse_mode="Markdown",
                )
            else:
                # Обрабатываем как обычный запрос
                await self.handle_search_request(update, context)
        else:
            # Любое другое сообщение считаем запросом на поиск
            await self.handle_search_request(update, context)

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        logger.error(f"Ошибка: {context.error}")

        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Произошла ошибка. Попробуйте еще раз."
            )

    def run(self):
        """Запуск бота"""
        logger.info("Запуск Telegram бота для поиска техники...")

        # Создаем приложение
        application = Application.builder().token(self.bot_token).build()

        # Добавляем обработчики
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("history", self.history_command))
        application.add_handler(CommandHandler("cancel", self.cancel_command))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        # Добавляем обработчик ошибок
        application.add_error_handler(self.error_handler)

        # Запускаем бота
        logger.info("Бот запущен. Ожидание сообщений...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Основная функция"""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не настроен")
        sys.exit(1)

    bot = TechSearchBot()
    bot.run()


if __name__ == "__main__":
    main()
