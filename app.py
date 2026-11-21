import re
from flask import Flask, request, make_response
from markupsafe import escape
from werkzeug.serving import WSGIRequestHandler

# Oculta versión de Werkzeug y Python en la cabecera Server (mitiga ZAP 10036)
WSGIRequestHandler.server_version = "SecureDev"
WSGIRequestHandler.sys_version = ""

app = Flask(__name__)

# Lista blanca: solo letras, números, espacios y guiones (máx. 50 caracteres)
NAME_PATTERN = re.compile(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s_-]{1,50}$')


@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; frame-ancestors 'none'; form-action 'self'"
    )
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    return response


@app.route('/')
def index():
    return "SecureDev API operativa", 200


@app.route('/hello')
def hello():
    name = request.args.get('name', 'Invitado').strip()
    if not NAME_PATTERN.match(name):
        return make_response("Parámetro 'name' inválido.", 400)
    safe_name = escape(name)
    return f"Hello, {safe_name}!", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)