#!/bin/bash

# Скрипт для запуска системы поиска техники

echo "🚀 Система поиска техники"
echo "========================"

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python3 для продолжения."
    exit 1
fi

# Проверяем наличие pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установите pip3 для продолжения."
    exit 1
fi

# Создаем виртуальное окружение если его нет
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
pip install -r requirements.txt

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден. Создаю из примера..."
    cp env_example.txt .env
    echo "📝 Отредактируйте файл .env, добавив токен Telegram бота и chat_id"
    echo "   Для получения токена: напишите @BotFather в Telegram"
    echo "   Для получения chat_id: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates"
    echo ""
    echo "Нажмите Enter после настройки .env файла..."
    read
fi

# Создаем директорию для данных
mkdir -p data

echo ""
echo "Выберите режим запуска:"
echo "1) Telegram бот (поиск по запросу)"
echo "2) Веб-интерфейс (админ-панель)"
echo "3) Ручной поиск"
echo "4) Демонстрация"
echo "5) Показать помощь"
echo ""

read -p "Введите номер (1-5): " choice

case $choice in
    1)
        echo "🤖 Запуск Telegram бота..."
        echo "   Напишите боту 'что ищем' или описание товара"
        echo "   Для остановки нажмите Ctrl+C"
        python main.py telegram-bot
        ;;
    2)
        echo "🌐 Запуск веб-интерфейса..."
        echo "   Веб-интерфейс будет доступен по адресу: http://localhost:5000"
        python main.py web
        ;;
    3)
        read -p "Введите запрос для поиска: " query
        if [ ! -z "$query" ]; then
            echo "🔍 Выполнение поиска: $query"
            python main.py search --query "$query"
        else
            echo "❌ Пустой запрос"
        fi
        ;;
    4)
        echo "🎯 Запуск демонстрации..."
        python demo.py
        ;;
    5)
        echo ""
        echo "📖 Помощь по использованию:"
        echo ""
        echo "Команды:"
        echo "  python main.py telegram-bot            - Запуск Telegram бота"
        echo "  python main.py web                     - Запуск веб-интерфейса"
        echo "  python main.py search -q 'запрос'      - Ручной поиск"
        echo "  python demo.py                         - Демонстрация"
        echo ""
        echo "Примеры запросов:"
        echo "  'Apple iPhone 15 PRO 256gb'"
        echo "  'Samsung Galaxy S24 128gb'"
        echo "  'MacBook Air M2 256gb'"
        echo "  'PlayStation 5'"
        echo ""
        ;;
    *)
        echo "❌ Неверный выбор"
        ;;
esac