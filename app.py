from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from cerebro.memoria import MemoriaLargoPlazo
from cerebro.red_neuronal import RedNeuronalPato
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

memoria = MemoriaLargoPlazo()
pato = RedNeuronalPato(memoria)

PASSWORD_ADMIN = "cuac123"

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("chat"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    if username:
        session["username"] = username
        return redirect(url_for("chat"))
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("admin", None)
    return redirect(url_for("index"))

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("index"))
    
    # Obtener historial del usuario actual para cargarlo en la vista
    historial = memoria.obtener_conversaciones_usuario(session["username"])
    return render_template("chat.html", username=session["username"], historial=historial, activo=pato.activo)

@app.route("/auth_admin", methods=["POST"])
def auth_admin():
    pwd = request.form.get("password", "")
    target = request.form.get("target", "historial")
    if pwd == PASSWORD_ADMIN:
        session["admin"] = True
        return redirect(url_for(target))
    return render_template("auth_error.html", target=target)

@app.route("/historial")
def historial():
    if not session.get("admin"):
        return render_template("admin_login.html", target="historial")
    filas = memoria.obtener_historial_completo()
    return render_template("history.html", historial=filas)

@app.route("/control")
def control():
    if not session.get("admin"):
        return render_template("admin_login.html", target="control")
    return render_template("control.html", activo=pato.activo)

# --- APIs ---
@app.route("/api/chat", methods=["POST"])
def api_chat():
    if "username" not in session:
        return jsonify({"error": "No autenticado"}), 401
        
    data = request.json
    mensaje_usuario = data.get("mensaje", "")
    username = session["username"]
    
    if mensaje_usuario:
        memoria.registrar_interaccion(username, "usuario", mensaje_usuario, pato.etapa)
    
    respuesta = pato.responder(mensaje_usuario)
    memoria.registrar_interaccion(username, "pato", respuesta, pato.etapa)
    
    return jsonify({"respuesta": respuesta, "etapa": pato.etapa, "activo": pato.activo})

@app.route("/api/toggle", methods=["POST"])
def api_toggle():
    if not session.get("admin"):
        return jsonify({"error": "No autorizado"}), 403
    data = request.json
    estado = data.get("estado")
    pato.activo = bool(estado)
    return jsonify({"success": True, "activo": pato.activo})

@app.route("/api/impulso", methods=["GET"])
def api_impulso():
    if "username" not in session: return jsonify({"impulso": ""})
    if not pato.activo: return jsonify({"impulso": ""})
    
    impulso = pato.generar_impulso()
    if impulso:
        memoria.registrar_interaccion(session["username"], "pato_autonomo", impulso, pato.etapa)
    return jsonify({"impulso": impulso})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
