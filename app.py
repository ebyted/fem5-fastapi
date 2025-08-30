from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import openai
import os
from prompts import get_prompt

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "*"]}, r"/dialogo": {"origins": ["http://localhost:5173", "*"]}})
openai.api_key = os.getenv("OPENAI_API_KEY")
@app.route('/dialogo', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://localhost:5173", "*"])
def dialogo():
    try:
        data = request.json
        mensaje = data.get('mensaje', '')
        nombre = data.get('nombre', '')
        fecha_nacimiento = data.get('fecha_nacimiento', '')
        hora_nacimiento = data.get('hora_nacimiento', '')
        lugar_nacimiento = data.get('lugar_nacimiento', '')

        # Si es la primera interacción, usar el prompt de bienvenida
        is_first_message = data.get('is_first_message', False)
        user_data = {
            "nombre": nombre,
            "fecha_nacimiento": fecha_nacimiento,
            "hora_nacimiento": hora_nacimiento,
            "lugar_nacimiento": lugar_nacimiento,
            "mensaje": mensaje
        }
        contexto = get_prompt("dialogo_sagrado", user_data)
        if is_first_message:
            prompt = contexto
        else:
            prompt = f"{contexto}\nUsuario: {mensaje}\nGuía responde:"
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=100
        )
        texto = response.choices[0].text.strip()
        print(f"Respuesta generada por el modelo: {texto}")
        return jsonify({"respuesta": texto})
    except Exception as e:
        import traceback
        print(f"Error en /dialogo: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/dialogo-sagrado/', methods=['POST'])
def dialogo_sagrado():
    try:
        data = request.json
        mensaje = data.get('mensaje', '')
        nombre = data.get('nombre', '')
        fecha_nacimiento = data.get('fecha_nacimiento', '')
        hora_nacimiento = data.get('hora_nacimiento', '')
        lugar_nacimiento = data.get('lugar_nacimiento', '')

        prompt = f"""Actúa como una guía espiritual simbólica, amorosa y presente. Estás dentro de la sección \"Diálogo Sagrado\" de la app BeCalm. El usuario escribe: \"{mensaje}\". Usa internamente estos datos: nombre: {nombre}, fecha: {fecha_nacimiento}, hora: {hora_nacimiento}, lugar: {lugar_nacimiento}. Responde canalizando simbólicamente su vibración actual, con tono suave y profundo, sin explicar ni pedir datos."""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120
        )
        texto = response.choices[0].message.content.strip()
        return jsonify({"respuesta": texto})
    except Exception as e:
        print(f"Error en /api/dialogo-sagrado/: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8034)
