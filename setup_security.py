#!/usr/bin/env python3
"""
Скрипт для безопасной настройки токенов
"""

import os
import sys
import shutil

def setup_security():
    """Настройка безопасности проекта"""
    print("🔒 Настройка безопасности проекта...")
    print("=" * 50)
    
    # 1. Проверяем наличие .env файла
    env_path = '.env'
    env_example_path = 'env_example.txt'
    
    if os.path.exists(env_path):
        print("✅ Файл .env уже существует")
        choice = input("❓ Перезаписать существующий .env файл? (y/N): ").lower()
        if choice != 'y':
            print("⏭️ Пропуск создания .env файла")
            return
    else:
        print("📝 Создание .env файла...")
    
    # 2. Копируем пример конфигурации
    try:
        shutil.copy(env_example_path, env_path)
        print("✅ Файл .env создан из env_example.txt")
    except FileNotFoundError:
        print("❌ Файл env_example.txt не найден!")
        return
    
    # 3. Запрашиваем токены у пользователя
    print("\n🔑 Настройка токенов:")
    print("Получите токен от @BotFather в Telegram")
    
    bot_token = input("📱 Введите TELEGRAM_BOT_TOKEN: ").strip()
    if not bot_token:
        print("❌ Токен бота не может быть пустым!")
        return
    
    chat_id = input("💬 Введите TELEGRAM_CHAT_ID: ").strip()
    if not chat_id:
        print("❌ Chat ID не может быть пустым!")
        return
    
    # 4. Обновляем .env файл
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Заменяем плейсхолдеры
        content = content.replace('YOUR_BOT_TOKEN_HERE', bot_token)
        content = content.replace('YOUR_CHAT_ID_HERE', chat_id)
        
        with open(env_path, 'w') as f:
            f.write(content)
        
        print("✅ Токены добавлены в .env файл")
        
    except Exception as e:
        print(f"❌ Ошибка обновления .env файла: {e}")
        return
    
    # 5. Проверяем .gitignore
    gitignore_path = '.gitignore'
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        if '.env' in gitignore_content:
            print("✅ .env файл добавлен в .gitignore")
        else:
            print("⚠️ .env файл НЕ добавлен в .gitignore!")
            print("💡 Добавьте '.env' в .gitignore файл")
    
    # 6. Проверяем права доступа
    try:
        os.chmod(env_path, 0o600)  # Только владелец может читать/писать
        print("✅ Права доступа к .env файлу установлены (600)")
    except Exception as e:
        print(f"⚠️ Не удалось установить права доступа: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Настройка безопасности завершена!")
    print("\n🛡️ Рекомендации:")
    print("1. Никогда не коммитьте .env файл в git")
    print("2. Регулярно обновляйте токены")
    print("3. Используйте разные токены для разных сред")
    print("4. Проверяйте логи на предмет утечек токенов")
    
    print("\n🚀 Теперь можно запустить бота:")
    print("python telegram_search_bot.py")

if __name__ == "__main__":
    setup_security()





