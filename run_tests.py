#!/usr/bin/env python3
"""
Скрипт для запуска тестов локально
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Запуск команды с выводом результата"""
    print(f"\n🔧 {description}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - УСПЕШНО")
        else:
            print(f"❌ {description} - ОШИБКА (код: {result.returncode})")
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Ошибка при выполнении: {e}")
        return False

def main():
    """Основная функция"""
    print("🧪 Запуск тестов проекта Tech Search Bot")
    print("=" * 60)
    
    # Проверяем, что мы в правильной директории
    if not os.path.exists('requirements.txt'):
        print("❌ Запустите скрипт из корневой папки проекта")
        sys.exit(1)
    
    # Устанавливаем зависимости
    if not run_command("pip install -r requirements.txt", "Установка зависимостей"):
        print("❌ Не удалось установить зависимости")
        sys.exit(1)
    
    # Запускаем тесты
    tests_passed = True
    
    # Базовые тесты
    tests_passed &= run_command("python tests/test_config.py", "Тесты конфигурации")
    tests_passed &= run_command("python tests/test_parsers.py", "Тесты парсеров")
    tests_passed &= run_command("python tests/test_search_engine.py", "Тесты поисковой системы")
    
    # Pytest тесты
    tests_passed &= run_command("pytest tests/ -v", "Pytest тесты")
    
    # Проверка кода
    tests_passed &= run_command("flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics", "Проверка критических ошибок")
    
    # Форматирование кода
    tests_passed &= run_command("black --check --diff .", "Проверка форматирования кода")
    
    # Безопасность
    tests_passed &= run_command("bandit -r . -ll", "Проверка безопасности")
    
    # Итоговый результат
    print("\n" + "=" * 60)
    if tests_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("✅ Проект готов к развертыванию")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ")
        print("🔧 Исправьте ошибки перед развертыванием")
        sys.exit(1)

if __name__ == "__main__":
    main()



