from flask import Flask, render_template, request, jsonify, redirect, url_for
from search_engine import SearchEngine
from telegram_bot import TelegramNotifier
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Инициализация компонентов
search_engine = SearchEngine()
telegram_notifier = TelegramNotifier()

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Выполнение поиска"""
    try:
        query = request.form.get('query', '').strip()
        if not query:
            return jsonify({'error': 'Введите запрос для поиска'}), 400
        
        # Выполняем поиск
        results = search_engine.search_all_stores(query)
        
        # Отправляем результаты в Telegram
        telegram_notifier.send_search_results_sync(results)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        error_msg = f"Ошибка при поиске: {str(e)}"
        telegram_notifier.send_error_notification_sync(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/history')
def history():
    """Страница истории поисков"""
    try:
        history = search_engine.get_search_history(20)
        return render_template('history.html', history=history)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/search/<int:query_id>')
def search_details(query_id):
    """Детальная информация о поиске"""
    try:
        details = search_engine.get_search_details(query_id)
        if not details:
            return render_template('error.html', error='Поиск не найден'), 404
        
        return render_template('search_details.html', details=details)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/search', methods=['POST'])
def api_search():
    """API для выполнения поиска"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Введите запрос для поиска'}), 400
        
        results = search_engine.search_all_stores(query)
        telegram_notifier.send_search_results_sync(results)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def api_history():
    """API для получения истории поисков"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = search_engine.get_search_history(limit)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/<int:query_id>')
def api_search_details(query_id):
    """API для получения детальной информации о поиске"""
    try:
        details = search_engine.get_search_details(query_id)
        if not details:
            return jsonify({'error': 'Поиск не найден'}), 404
        
        return jsonify(details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    from config.settings import WEB_HOST, WEB_PORT, DEBUG
    app.run(host=WEB_HOST, port=WEB_PORT, debug=DEBUG)




