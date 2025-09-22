#!/usr/bin/env python3
"""
Тесты парсеров
"""

import os
import sys
import pytest

# Добавляем корневую папку в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_parser_imports():
    """Тест импорта всех парсеров"""
    try:
        from parsers.pitergsm_parser import PiterGSMParser
        from parsers.world_devices_parser import WorldDevicesParser
        from parsers.gsm_store_parser import GSMStoreParser
        from parsers.dns_parser import DNSParser
        from parsers.mvideo_parser import MVideoParser
        from parsers.eldorado_parser import EldoradoParser
        from parsers.citilink_parser import CitilinkParser

        print("✅ Все парсеры импортированы успешно")
    except ImportError as e:
        pytest.fail(f"Ошибка импорта парсеров: {e}")


def test_parser_initialization():
    """Тест инициализации парсеров"""
    try:
        from parsers.pitergsm_parser import PiterGSMParser
        from parsers.world_devices_parser import WorldDevicesParser

        # Тестируем инициализацию
        pitergsm = PiterGSMParser()
        world_devices = WorldDevicesParser()

        assert pitergsm.store_name == "PiterGSM"
        assert world_devices.store_name == "World Devices"

        print("✅ Парсеры инициализированы корректно")
    except Exception as e:
        pytest.fail(f"Ошибка инициализации парсеров: {e}")


def test_base_parser():
    """Тест базового парсера"""
    try:
        from parsers.base_parser import BaseParser

        class TestParser(BaseParser):
            def __init__(self):
                super().__init__("Test Store")

            def search_products(self, query):
                return []

            def parse_product(self, product_element):
                return None

        parser = TestParser()
        assert parser.store_name == "Test Store"
        assert hasattr(parser, "session")
        assert hasattr(parser, "get_page")

        print("✅ Базовый парсер работает корректно")
    except Exception as e:
        pytest.fail(f"Ошибка базового парсера: {e}")


def test_parser_methods():
    """Тест методов парсеров"""
    try:
        from parsers.world_devices_parser import WorldDevicesParser

        parser = WorldDevicesParser()

        # Проверяем наличие методов
        assert hasattr(parser, "search_products")
        assert hasattr(parser, "parse_product")
        assert callable(parser.search_products)
        assert callable(parser.parse_product)

        print("✅ Методы парсеров определены корректно")
    except Exception as e:
        pytest.fail(f"Ошибка методов парсеров: {e}")


if __name__ == "__main__":
    test_parser_imports()
    test_parser_initialization()
    test_base_parser()
    test_parser_methods()
    print("🎉 Все тесты парсеров прошли успешно!")
