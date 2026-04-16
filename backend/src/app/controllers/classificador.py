from flask import Blueprint, jsonify, request

from app.prompts import ClassificadorPrompts
from app.schemas.classificador import AnalisePerfil, ClassificadorFormRequestSchema
from app.services import GeminiService

bp = Blueprint("classificador", __name__, url_prefix="/classificador")


@bp.post("/analisar-perfil")
def classificar():
    data = request.get_json()
    schema = ClassificadorFormRequestSchema()
    errors = schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    prompt: str = ClassificadorPrompts.classificar(data)

    resultado: dict = GeminiService.generate(prompt)

    schema = AnalisePerfil()
    schema.validate(resultado)

    return jsonify(resultado)
