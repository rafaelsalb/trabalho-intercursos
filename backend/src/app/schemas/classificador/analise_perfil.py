from marshmallow import fields

from app.schemas.json import JsonResponseSchema


class AnalisePerfil(JsonResponseSchema):
    classificacao_pj = fields.Str(required=True)
    setor_atuacao = fields.Str(
        required=True, validate=lambda x: x in ["Serviços", "Comércio", "Indústria"]
    )
    perfil_resumo = fields.Str()
    justificativa_enquadramento = fields.Str()
    cnae_principal = fields.Str()
    cnaes_secundarios = fields.List(fields.Str())
    alerta_impeditivo = fields.Str(allow_none=True)
