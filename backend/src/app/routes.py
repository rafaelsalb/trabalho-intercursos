from flask import Blueprint, request

from .controllers import auth, classificador

bp = Blueprint("index", __name__, url_prefix="/api/v1")


@bp.get("/")
def index():
    return "Hello, world!"


@bp.get("/health")
def health():
    return "Healthy", 200


@bp.post("/echo")
def echo():
    message = request.json.get("message", "")
    return {"message": message}


def register_blueprints(app):
    """
    Registre todos os blueprints aqui
    """
    bp.register_blueprint(auth.bp)
    bp.register_blueprint(classificador.bp)
    app.register_blueprint(bp)
