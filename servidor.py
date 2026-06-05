"""
Servidor local de pruebas para el experimento CookieJar (Actualizado para AUDIO).
Emula los endpoints de datapruebas.org para recibir audios puros y datos de jsPsych.
Modificado para dar soporte al almacenamiento exclusivo de archivos de audio en el puerto 8002.
"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Creamos la carpeta específica donde se guardarán los audios si no existe
CARPETA_GRABACIONES = '/Users/berni/Desktop/audios_cookiejar'
os.makedirs(CARPETA_GRABACIONES, exist_ok=True)

# Configuración de cabeceras para permitir CORS (Cross-Origin Resource Sharing)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-CSRFToken')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# =========================================================================
# ENDPOINT DE AUDIO: Recibe el archivo de audio (.webm)
# =========================================================================
@app.route('/api/v1/record_audio/<run_id>/', methods=['POST', 'OPTIONS'])
def record_audio(run_id):
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
        
    print(f"\n🎙️ [AUDIO] Petición entrante para la sesión (run-id): {run_id}")
    
    # Comprobamos que el archivo venga bajo la clave 'audio' (exigencia del script recordAudio)
    if 'audio' not in request.files:
        print("❌ Error: No se encontró la clave de archivo esperada en el payload.")
        return jsonify({"status": "FAIL", "error": "Falta archivo de audio"}), 400
        
    archivo = request.files['audio']
    if archivo.filename == '':
        print("❌ Error: Nombre de archivo vacío.")
        return jsonify({"status": "FAIL", "error": "Nombre de archivo vacío"}), 400

    # Construimos la ruta de destino y guardamos el archivo de audio físico en el disco
    ruta_guardado = os.path.join(CARPETA_GRABACIONES, archivo.filename)
    archivo.save(ruta_guardado)
    
    print(f"✅ ¡Audio de la descripción guardado con éxito localmente!")
    print(f"   📂 Ubicación: {ruta_guardado}")
    return jsonify({"status": "OK"}), 200


# 2. Endpoint para recibir las métricas cualitativas de jsPsych (tiempos de reacción, etc.)
@app.route('/api/v1/record_data/<run_id>/', methods=['POST', 'OPTIONS'])
def record_data(run_id):
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
        
    datos = request.json
    print(f"\n[DATOS] Métricas cualitativas recibidas para run-id [{run_id}]:")
    print(f"   📊 Contenido: {datos}")
    return jsonify({"status": "OK"}), 200


# 3. Endpoint para finalizar la corrida experimental (Fin de la Parte 1 o Parte 2)
@app.route('/api/v1/end_run/<run_id>/', methods=['POST', 'OPTIONS'])
def end_run(run_id):
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200
        
    datos = request.json if request.is_json else {}
    print(f"\n🏁 [FIN] Notificación de cierre recibida para run-id [{run_id}].")
    print(f"   🏆 Puntaje final (si aplica): {datos.get('score', 'No aplica/Solo texto')}")
    return jsonify({"status": "OK"}), 200


if __name__ == '__main__':
    print("====================================================")
    print("  Iniciando Servidor de Pruebas Local (AUDIO ONLY)  ")
    print("  Compatible con el nuevo setup del experimento   ")
    print("  Escuchando en: http://localhost:8002              ")
    print("====================================================")
    app.run(port=8002, debug=True)