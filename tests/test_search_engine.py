#!/usr/bin/env python3
"""
Тесты поисковой системы
"""

import os
import sys
import pytest

# Добавляем корневую папку в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_search_engine_import():
    """Тест импорта поисковой системы"""
    try:
        from search_engine import SearchEngine

        print("✅ Поисковая система импортирована успешно")
    except ImportError as e:
        pytest.fail(f"Ошибка импорта поисковой системы: {e}")


def test_search_engine_initialization():
    """Тест инициализации поисковой системы"""
    try:
        from search_engine import SearchEngine

        engine = SearchEngine()
        assert hasattr(engine, "parsers")
        assert isinstance(engine.parsers, dict)

        print("✅ Поисковая система инициализирована корректно")
    except Exception as e:
        pytest.fail(f"Ошибка инициализации поисковой системы: {e}")


def test_search_engine_methods():
    """Тест методов поисковой системы"""
    try:
        from search_engine import SearchEngine

        engine = SearchEngine()

        # Проверяем наличие методов
        assert hasattr(engine, "search_all_stores")
        assert hasattr(engine, "init_database")
        assert callable(engine.search_all_stores)
        assert callable(engine.init_database)

        print("✅ Методы поисковой системы определены корректно")
    except Exception as e:
        pytest.fail(f"Ошибка методов поисковой системы: {e}")


def test_database_initialization():
    """Тест инициализации базы данных"""
    try:
        from search_engine import SearchEngine

        engine = SearchEngine()
        # Тестируем инициализацию БД (без создания реального файла)
        engine.init_database()

        print("✅ База данных инициализирована корректно")
    except Exception as e:
        pytest.fail(f"Ошибка инициализации базы данных: {e}")


if __name__ == "__main__":
    test_search_engine_import()
    test_search_engine_initialization()
    test_search_engine_methods()
    test_database_initialization()
    print("🎉 Все тесты поисковой системы прошли успешно!")
