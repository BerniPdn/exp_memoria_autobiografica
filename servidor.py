"""
Servidor local de pruebas para el experimento de Memoria Autobiográfica.
Sirve archivos estáticos Y recibe audios/datos — un solo comando para todo.
"""

import os
from flask import Flask, request, jsonify, send_from_directory

CARPETA_EXPERIMENTO = os.path.dirname(os.path.abspath(__file__))
CARPETA_GRABACIONES = '/Users/berni/Desktop/audios_cookiejar'
os.makedirs(CARPETA_GRABACIONES, exist_ok=True)

app = Flask(__name__, static_folder=CARPETA_EXPERIMENTO)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-CSRFToken')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# ── Archivos estáticos ──────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(CARPETA_EXPERIMENTO, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(CARPETA_EXPERIMENTO, filename)

# ── API ─────────────────────────────────────────────────────────────────────
@app.route('/api/v1/record_audio/<run_id>/', methods=['POST', 'OPTIONS'])
def record_audio(run_id):
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    print(f"\n🎙️ [AUDIO] run-id: {run_id}")
    if 'audio' not in request.files:
        return jsonify({"status": "FAIL", "error": "Falta archivo de audio"}), 400
    archivo = request.files['audio']
    if archivo.filename == '':
        return jsonify({"status": "FAIL", "error": "Nombre vacío"}), 400
    ruta = os.path.join(CARPETA_GRABACIONES, archivo.filename)
    archivo.save(ruta)
    print(f"✅ Audio guardado: {ruta}")
    return jsonify({"status": "OK"}), 200

@app.route('/api/v1/record_data/<run_id>/', methods=['POST', 'OPTIONS'])
def record_data(run_id):
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    print(f"\n[DATOS] run-id [{run_id}]: {request.json}")
    return jsonify({"status": "OK"}), 200

@app.route('/api/v1/end_run/<run_id>/', methods=['POST', 'OPTIONS'])
def end_run(run_id):
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
    datos = request.json if request.is_json else {}
    print(f"\n🏁 [FIN] run-id [{run_id}]. Score: {datos.get('score', 'N/A')}")
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    print("====================================================")
    print("  Servidor unificado — experimento + API            ")
    print("  Abrí: http://localhost:8002?run-id=test_berni     ")
    print("====================================================")
    app.run(port=8002, debug=True)