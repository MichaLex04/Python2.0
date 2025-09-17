# py/app.py
from flask import Flask, jsonify, request
from py import recetas, api_deepseek

app = Flask(__name__)

@app.route("/api/recetas", methods=["GET"])
def api_listar_recetas():
    recetas_list = recetas.listar_recetas()
    return jsonify(recetas_list)

@app.route("/api/calcular", methods=["GET"])
def api_calcular():
    receta_id = request.args.get("receta_id", type=int)
    personas = request.args.get("personas", type=int)
    if not receta_id or not personas:
        return jsonify({"error": "Parámetros inválidos"}), 400
    try:
        ingredientes = recetas.calcular_cantidades(receta_id, personas)
        return jsonify({"ingredientes": ingredientes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generar_receta", methods=["POST"])
def api_generar_receta():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Falta prompt"}), 400
    try:
        receta_texto = api_deepseek.generar_receta_ia(prompt)
        return jsonify({"receta_texto": receta_texto})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/guardar_receta", methods=["POST"])
def api_guardar_receta():
    data = request.get_json()
    receta_texto = data.get("receta_texto")