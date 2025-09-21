# 🔍 Tech Search Bot - Поиск техники через Telegram

Telegram бот для поиска и сравнения цен на технику в различных интернет-магазинах. Работает только по запросу пользователя через удобный двухэтапный интерфейс.

## ✨ Возможности

- 🤖 **Telegram бот** с интуитивным интерфейсом
- 🔍 **Поиск по 7 магазинам** одновременно
- 💰 **Топ-3 самых дешевых** результата с ценами и ссылками
- 📱 **Отправка результатов в Telegram** в удобном формате
- ⏱️ **Реалистичные задержки** для обхода блокировок
- 📊 **История поисков** в базе данных SQLite
- 🎛️ **Управление состояниями** пользователей

## 🏪 Поддерживаемые магазины

1. **PiterGSM** ✅
2. **World Devices** ✅  
3. **GSM Store** ⚠️
4. **DNS** ⚠️
5. **М.Видео** ⚠️
6. **Эльдорадо** ⚠️
7. **Ситилинк** ⚠️

*⚠️ Некоторые магазины могут блокировать автоматические запросы*

## 📱 Как пользоваться

### Двухэтапный процесс поиска:

1. **Этап 1:** Напишите боту `что ищем` или `поиск товара`
2. **Этап 2:** Отправьте описание товара
3. **Этап 3:** Получите результаты поиска

### Команды бота:
- `/start` - начать работу
- `/help` - справка
- `/history` - история поисков
- `/cancel` - отменить поиск

### Примеры запросов:
```
iPhone 15 PRO 256gb
Dyson Complete Long
MacBook Air M2 256gb
PlayStation 5
Samsung Galaxy S24
AirPods Pro 2
```

## 🚀 Быстрая установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/andreympototskiy-code/tech-search-bot.git
cd tech-search-bot
```

### 2. Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка Telegram бота

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен бота
3. Создайте файл `.env`:
```bash
cp env_example.txt .env
```

4. Отредактируйте `.env`, добавив токены:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 5. Запуск
```bash
./run_bot.sh
```

Или вручную:
```bash
python main.py telegram-bot
```

## 📁 Структура проекта

```
tech-search/
├── config/
│   └── settings.py              # Настройки приложения
├── parsers/                     # Парсеры магазинов
│   ├── base_parser.py          # Базовый класс с улучшениями
│   ├── world_devices_parser.py # World Devices
│   ├── gsm_store_parser.py     # GSM Store
│   ├── pitergsm_parser.py      # PiterGSM
│   └── ...                     # Другие парсеры
├── web_interface/              # Веб-интерфейс (опционально)
├── telegram_search_bot.py     # Telegram бот
├── search_engine.py           # Движок поиска
├── main.py                    # Основной запуск
├── run_bot.sh                 # Быстрый запуск бота
├── requirements.txt           # Зависимости Python
└── README.md                  # Этот файл
```

## ⚙️ Технические особенности

### Улучшения для обхода блокировок:
- **Реалистичные заголовки** (Chrome 120, полный набор заголовков)
- **Увеличенные задержки** (3-8 секунд между запросами)
- **Referer заголовки** для каждого магазина
- **Timeout 15 секунд** на запрос
- **До 3 попыток** при ошибках

### Архитектура:
- **Асинхронный Telegram бот** на python-telegram-bot
- **Управление состояниями** пользователей
- **SQLite база данных** для истории поисков
- **Модульная архитектура** парсеров
- **Обработка ошибок** и логирование

## 🔧 Команды разработчика

```bash
# Запуск бота
python main.py telegram-bot

# Веб-интерфейс (для администрирования)
python main.py web

# Ручной поиск (для тестирования)
python main.py search --query "iPhone 15 PRO"

# Демонстрация
python demo.py

# Тестирование Telegram
python test_telegram.py
```

## 📊 Пример работы

```
👤 Пользователь: что ищем

🤖 Бот: 📝 Опишите товар, который хотите найти

Примеры запросов:
• iPhone 15 PRO 256gb
• Dyson Complete Long
• MacBook Air M2 256gb

👤 Пользователь: iPhone 15 PRO 256gb

🤖 Бот: 🔍 Результаты поиска: iPhone 15 PRO 256gb

📊 Найдено товаров: 15
⏰ Время поиска: 14:30:25

🏆 Топ 3 самых дешевых:

1. iPhone 15 PRO 256gb Space Black
💰 Цена: 89,990 ₽
🏪 Магазин: PiterGSM
🔗 Перейти к товару

2. iPhone 15 PRO 256gb Natural Titanium  
💰 Цена: 91,500 ₽
🏪 Магазин: World Devices
🔗 Перейти к товару

3. iPhone 15 PRO 256gb Blue Titanium
💰 Цена: 92,000 ₽
🏪 Магазин: GSM Store
🔗 Перейти к товару
```

## 🚨 Важные замечания

### Безопасность:
- **Не публикуйте токены** в открытом доступе
- **Используйте .env файл** для хранения секретов
- **Добавьте .env в .gitignore**

### Ограничения:
- Некоторые сайты блокируют автоматические запросы
- Результаты могут зависеть от доступности магазинов
- Парсеры могут требовать обновления при изменении структуры сайтов

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте ветку для новой функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 👨‍💻 Автор

**Andrey Pototskiy** - [@andreympototskiy-code](https://github.com/andreympototskiy-code)

## 📞 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте [Issues](https://github.com/andreympototskiy-code/tech-search-bot/issues)
2. Создайте новый Issue с описанием проблемы
3. Приложите логи и скриншоты

---

**Удачного поиска техники!** 🔍📱💻