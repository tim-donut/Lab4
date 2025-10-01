import os
import json # Использовать безопасный JSON вместо pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- ИСПРАВЛЕНИЕ: Секреты (Secrets) ---
# Секреты нужно читать из переменных окружения (Environment Variables)
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "DefaultSecureFallback123")
# Примечание: Для продакшена нужно обеспечить, чтобы DATABASE_PASSWORD всегда была установлена!

# --- ИСПРАВЛЕНИЕ: Раскрытие информации в ошибках (Errors) ---
# Отключить режим отладки для продакшена и использовать обработчик ошибок
app.config['DEBUG'] = False # Отключить отладку

@app.errorhandler(500)
def internal_error(error):
    # Кастомный обработчик, который не раскрывает внутренний трассировочный след
    return jsonify({"error": "Внутренняя ошибка сервера. Приносим извинения."}), 500

@app.route('/')
def home():
    return "Сервер запущен. Проверьте /error, /secret, /deserialize"

@app.route('/error')
def trigger_error():
    # Теперь ошибка будет обработана кастомным обработчиком 500
    try:
        return "Результат: " + str(10 / 0)
    except Exception:
        # Для демонстрации вызовем ошибку 500
        return internal_error(500)


@app.route('/secret')
def check_secret():
    # Использование секрета из безопасного места
    if request.args.get('key') == DATABASE_PASSWORD:
        return jsonify({"message": "Доступ разрешен"}), 200
    return jsonify({"message": "Доступ запрещен"}), 403


# --- ИСПРАВЛЕНИЕ: Небезопасная десериализация (Insecure Deserialization) ---
@app.route('/deserialize', methods=['POST'])
def secure_deserialization():
    # Использовать безопасный формат данных (JSON) вместо pickle
    data = request.data
    try:
        # Используем json.loads, который не выполняет произвольный код
        deserialized_data = json.loads(data)
        return jsonify({"message": "Объект успешно десериализован с помощью JSON", "data": str(deserialized_data)}), 200
    except Exception as e:
        # Для безопасности не раскрываем детали ошибки
        return jsonify({"error": "Ошибка обработки данных. Неверный формат."}), 400

if __name__ == '__main__':
    # В продакшене не запускаем с debug=True
    app.run(port=5000)