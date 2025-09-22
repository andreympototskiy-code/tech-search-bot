import sqlite3
import json
from datetime import datetime
from typing import List, Dict
from parsers.pitergsm_parser import PiterGSMParser
from parsers.world_devices_parser import WorldDevicesParser
from parsers.gsm_store_parser import GSMStoreParser
from parsers.dns_parser import DNSParser
from parsers.mvideo_parser import MVideoParser
from parsers.eldorado_parser import EldoradoParser
from parsers.citilink_parser import CitilinkParser
from config.settings import STORES, MAX_RESULTS, DATABASE_PATH
import os


class SearchEngine:
    def __init__(self):
        self.parsers = {
            "pitergsm": PiterGSMParser(),
            "world_devices": WorldDevicesParser(),
            "gsm_store": GSMStoreParser(),
            "dns": DNSParser(),
            "mvideo": MVideoParser(),
            "eldorado": EldoradoParser(),
            "citilink": CitilinkParser(),
        }
        self.init_database()

    def init_database(self):
        """Инициализация базы данных"""
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS search_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS search_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER,
                store_name TEXT NOT NULL,
                title TEXT NOT NULL,
                price INTEGER NOT NULL,
                link TEXT NOT NULL,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (query_id) REFERENCES search_queries (id)
            )
        """
        )

        conn.commit()
        conn.close()

    def search_all_stores(self, query: str) -> Dict:
        """Поиск по всем магазинам"""
        print(f"Начинаем поиск: {query}")

        # Сохраняем запрос в базу данных
        query_id = self.save_query(query)

        all_results = []
        store_results = {}

        for store in STORES:
            store_name = store["name"]
            parser_name = store["parser"]

            print(f"Поиск в {store_name}...")

            try:
                if parser_name in self.parsers:
                    parser = self.parsers[parser_name]
                    results = parser.search_products(query)

                    # Сохраняем результаты в базу данных
                    for result in results:
                        self.save_result(query_id, result)

                    store_results[store_name] = results
                    all_results.extend(results)

                    print(f"Найдено {len(results)} товаров в {store_name}")
                else:
                    print(f"Парсер для {store_name} не найден")

            except Exception as e:
                print(f"Ошибка при поиске в {store_name}: {e}")
                store_results[store_name] = []

        # Сортируем по цене и берем топ результатов
        all_results.sort(key=lambda x: x["price"])
        top_results = all_results[:MAX_RESULTS]

        return {
            "query": query,
            "query_id": query_id,
            "total_found": len(all_results),
            "top_results": top_results,
            "store_results": store_results,
            "search_time": datetime.now().isoformat(),
        }

    def save_query(self, query: str) -> int:
        """Сохранение запроса в базу данных"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO search_queries (query) VALUES (?)", (query,))
        query_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return query_id

    def save_result(self, query_id: int, result: Dict):
        """Сохранение результата поиска в базу данных"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO search_results (query_id, store_name, title, price, link)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                query_id,
                result["store"],
                result["title"],
                result["price"],
                result["link"],
            ),
        )

        conn.commit()
        conn.close()

    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """Получение истории поисков"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT sq.id, sq.query, sq.created_at, COUNT(sr.id) as results_count
            FROM search_queries sq
            LEFT JOIN search_results sr ON sq.id = sr.query_id
            GROUP BY sq.id
            ORDER BY sq.created_at DESC
            LIMIT ?
        """,
            (limit,),
        )

        results = []
        for row in cursor.fetchall():
            results.append(
                {
                    "id": row[0],
                    "query": row[1],
                    "created_at": row[2],
                    "results_count": row[3],
                }
            )

        conn.close()
        return results

    def get_search_details(self, query_id: int) -> Dict:
        """Получение детальной информации о поиске"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Получаем информацию о запросе
        cursor.execute(
            "SELECT query, created_at FROM search_queries WHERE id = ?", (query_id,)
        )
        query_info = cursor.fetchone()

        if not query_info:
            return None

        # Получаем результаты поиска
        cursor.execute(
            """
            SELECT store_name, title, price, link, found_at
            FROM search_results
            WHERE query_id = ?
            ORDER BY price ASC
        """,
            (query_id,),
        )

        results = []
        for row in cursor.fetchall():
            results.append(
                {
                    "store": row[0],
                    "title": row[1],
                    "price": row[2],
                    "link": row[3],
                    "found_at": row[4],
                }
            )

        conn.close()

        return {"query": query_info[0], "created_at": query_info[1], "results": results}
