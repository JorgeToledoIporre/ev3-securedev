import re
from flask import Flask, request, make_response
from markupsafe import escape
from werkzeug.serving import WSGIRequestHandler
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

WSGIRequestHandler.server_version = "SecureDev"
WSGIRequestHandler.sys_version = ""

app = Flask(__name__)

NAME_PATTERN = re.compile(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s_-]{1,50}$')

REQUEST_COUNT = Counter(
    'app_http_requests_total',
    'Total de peticiones HTTP recibidas',
    ['endpoint', 'status']
)
SECURITY_ALERTS = Counter(
    'app_security_blocked_total',
    'Total de intentos de ataque XSS bloqueados'
)


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
    REQUEST_COUNT.labels(endpoint='/', status='200').inc()
    return "SecureDev API operativa", 200


@app.route('/hello')
def hello():
    name = request.args.get('name', 'Invitado').strip()
    if not NAME_PATTERN.match(name):
        SECURITY_ALERTS.inc()
        REQUEST_COUNT.labels(endpoint='/hello', status='400').inc()
        return make_response("Parámetro 'name' inválido.", 400)
    REQUEST_COUNT.labels(endpoint='/hello', status='200').inc()
    safe_name = escape(name)
    return f"Hello, {safe_name}!", 200


@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)