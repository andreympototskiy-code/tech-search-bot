#!/bin/bash

# Скрипт для быстрого запуска Telegram бота

echo "🤖 Запуск Telegram бота для поиска техники"
echo "=========================================="

# Переходим в директорию проекта
cd /root/tech-search

# Проверяем виртуальное окружение
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено"
    echo "Запустите сначала: ./start.sh"
    exit 1
fi

# Активируем виртуальное окружение
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Проверяем токен бота
if grep -q "8443193400" config/settings.py; then
    echo "✅ Telegram бот настроен"
else
    echo "❌ Telegram бот не настроен"
    exit 1
fi

echo ""
echo "📱 Telegram бот запускается..."
echo "Напишите боту 'что ищем' или описание товара"
echo "Для остановки нажмите Ctrl+C"
echo ""

# Запускаем бота
python main.py telegram-bot








