import os
import pickle
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE_PASSWORD = "password12345"

@app.route('/')
def home():
    return "Сервер запущен. Проверьте /error, /secret, /deserialize"

@app.route('/error')
def trigger_error():
    return "Результат: " + str(10 / 0) 
@app.route('/secret')
def check_secret():
    if request.args.get('key') == DATABASE_PASSWORD:
        return jsonify({"message": "Доступ разрешен. Пароль: " + DATABASE_PASSWORD}), 200
    return jsonify({"message": "Доступ запрещен"}), 403


@app.route('/deserialize', methods=['POST'])
def insecure_deserialization():
    data = request.data
    try:
        deserialized_data = pickle.loads(base64.b64decode(data))
        return jsonify({"message": "Объект успешно десериализован", "data": str(deserialized_data)}), 200
    except Exception as e:
        return jsonify({"error": "Ошибка десериализации", "details": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)