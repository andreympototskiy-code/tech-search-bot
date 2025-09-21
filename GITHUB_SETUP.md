# 🚀 Инструкция по выгрузке в GitHub

## 📋 Шаги для создания репозитория

### 1. Создание репозитория на GitHub

1. Перейдите на https://github.com/andreympototskiy-code
2. Нажмите кнопку **"New"** или **"+"** → **"New repository"**
3. Заполните форму:
   - **Repository name**: `tech-search-bot`
   - **Description**: `Telegram bot for tech price comparison across multiple online stores`
   - **Visibility**: Public (или Private)
   - **Initialize**: НЕ отмечайте галочки (README, .gitignore, license)
4. Нажмите **"Create repository"**

### 2. Выгрузка кода

После создания репозитория выполните команды:

```bash
cd /root/tech-search

# Проверьте статус
git status

# Отправьте в GitHub
git push -u origin main
```

### 3. Альтернативный способ (если нужна авторизация)

Если GitHub требует авторизацию:

```bash
# Установите GitHub CLI (если не установлен)
# curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
# echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
# sudo apt update
# sudo apt install gh

# Авторизуйтесь в GitHub
gh auth login

# Создайте репозиторий через CLI
gh repo create andreympototskiy-code/tech-search-bot --public --source=. --remote=origin --push
```

## 📁 Что будет в репозитории

### Основные файлы:
- `README.md` - подробное описание проекта
- `LICENSE` - MIT лицензия
- `requirements.txt` - зависимости Python
- `.gitignore` - исключения для git

### Код проекта:
- `telegram_search_bot.py` - основной Telegram бот
- `search_engine.py` - движок поиска
- `parsers/` - парсеры для магазинов
- `web_interface/` - веб-интерфейс
- `config/` - настройки

### Скрипты:
- `run_bot.sh` - быстрый запуск бота
- `start.sh` - полный скрипт установки
- `main.py` - основной файл запуска

### Документация:
- `TELEGRAM_BOT_GUIDE.md` - руководство по боту
- `SEARCH_FLOW_GUIDE.md` - описание процесса поиска
- `TESTING_NEW_STORES.md` - тестирование магазинов
- `SETUP_COMPLETE.md` - завершение настройки

## 🔗 Ссылки после создания

После успешной выгрузки репозиторий будет доступен по адресу:
**https://github.com/andreympototskiy-code/tech-search-bot**

### Возможности:
- 📖 Просмотр кода онлайн
- 📥 Клонирование репозитория
- 🐛 Создание Issues
- 🔄 Pull Requests
- 📊 Статистика проекта
- 🏷️ Релизы и теги

## ✅ Проверка успешной выгрузки

После выполнения команд проверьте:

1. **GitHub репозиторий** создан и содержит файлы
2. **README.md** отображается корректно
3. **Все файлы** загружены
4. **История коммитов** сохранена

## 🎯 Готово!

Проект будет доступен всем пользователям GitHub с подробной документацией и инструкциями по установке.

