#!/usr/bin/env python3
"""
Отладка PiterGSM для понимания проблемы с декодированием
"""

import sys
import os
sys.path.append('.')

from parsers.pitergsm_parser import PiterGSMParser
import requests

def debug_pitergsm():
    """Отладка PiterGSM"""
    print("🔍 Отладка PiterGSM")
    print("=" * 50)
    
    parser = PiterGSMParser()
    query = "iPhone 15 PRO 256gb"
    search_url = f"https://pitergsm.ru/?digiSearch=true&term={query}&params=%7Csort%3DDEFAULT"
    
    response = parser.get_page(search_url)
    if not response:
        print("❌ Не удалось получить страницу")
        return
    
    print(f"📊 Статус: {response.status_code}")
    print(f"📏 Размер response.text: {len(response.text)}")
    print(f"📏 Размер response.content: {len(response.content)}")
    print(f"🔗 URL: {response.url}")
    print(f"📄 Content-Type: {response.headers.get('content-type', 'Не указан')}")
    print(f"📄 Content-Encoding: {response.headers.get('content-encoding', 'Не указан')}")
    
    # Проверяем первые символы
    print(f"\n🔍 Первые 200 символов response.text:")
    print(repr(response.text[:200]))
    
    print(f"\n🔍 Первые 200 символов response.content:")
    print(repr(response.content[:200]))
    
    # Пробуем разные кодировки
    try:
        decoded_utf8 = response.content.decode('utf-8')
        print(f"\n✅ UTF-8 декодирование: {len(decoded_utf8)} символов")
        print(f"Первые 200 символов UTF-8: {repr(decoded_utf8[:200])}")
    except Exception as e:
        print(f"\n❌ UTF-8 декодирование: {e}")
    
    try:
        decoded_windows = response.content.decode('windows-1251')
        print(f"\n✅ Windows-1251 декодирование: {len(decoded_windows)} символов")
        print(f"Первые 200 символов Windows-1251: {repr(decoded_windows[:200])}")
    except Exception as e:
        print(f"\n❌ Windows-1251 декодирование: {e}")

if __name__ == "__main__":
    debug_pitergsm()
