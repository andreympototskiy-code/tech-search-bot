#!/usr/bin/env python3
"""
Тесты конфигурации
"""

import os
import sys
import pytest

# Добавляем корневую папку в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_settings_import():
    """Тест импорта настроек"""
    try:
        from config.settings import SEARCH_INTERVAL_HOURS, MAX_RESULTS, REQUEST_DELAY_SECONDS
        assert SEARCH_INTERVAL_HOURS == 0, "Автоматический поиск должен быть отключен"
        assert MAX_RESULTS == 3, "Максимум результатов должен быть 3"
        assert REQUEST_DELAY_SECONDS == 20, "Задержка между запросами должна быть 20 секунд"
        print("✅ Настройки корректны")
    except Exception as e:
        pytest.fail(f"Ошибка импорта настроек: {e}")

def test_telegram_tokens_required():
    """Тест требований токенов Telegram"""
    try:
        from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
        # Если токены не установлены, должно быть исключение
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            pytest.fail("Токены Telegram должны быть установлены")
    except ValueError as e:
        # Это ожидаемое поведение если токены не установлены
        assert "TELEGRAM_BOT_TOKEN" in str(e) or "TELEGRAM_CHAT_ID" in str(e)
        print("✅ Проверка токенов работает корректно")

def test_stores_configuration():
    """Тест конфигурации магазинов"""
    try:
        from config.settings import STORES
        assert isinstance(STORES, list), "STORES должен быть списком"
        assert len(STORES) > 0, "Должен быть хотя бы один магазин"
        
        for store in STORES:
            assert 'name' in store, "Магазин должен иметь имя"
            assert 'url' in store, "Магазин должен иметь URL"
            assert 'search_url' in store, "Магазин должен иметь URL поиска"
            assert 'parser' in store, "Магазин должен иметь парсер"
        
        print("✅ Конфигурация магазинов корректна")
    except Exception as e:
        pytest.fail(f"Ошибка конфигурации магазинов: {e}")

if __name__ == "__main__":
    test_settings_import()
    test_telegram_tokens_required()
    test_stores_configuration()
    print("🎉 Все тесты конфигурации прошли успешно!")



