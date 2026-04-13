import json

from google import genai
from google.genai import types

from ..config import Config


class GeminiService:
    @staticmethod
    def generate(data: str) -> str:
        client = genai.Client(
            api_key=Config.GEMINI_API_KEY,
        )

        model = "gemini-2.5-flash-lite"
        system_instruction = (
            "Você é um consultor contábil especializado em legislação "
            "empresarial brasileira e CNAEs. Sua função é analisar "
            "o relato de um empreendedor e classificar seu negócio "
            "em MEI ou ME, sugerindo "
            "os códigos CNAE correspondentes."
            ""
            "### REGRAS DE CLASSIFICAÇÃO:"
            "1. **MEI (Microempreendedor Individual):**"
            "- Limite: R$ 81.000,00/ano e 1 funcionário."
            "- Atividades: Operacionais e braçais. "
            "- **IMPEDIMENTO:** Profissões regulamentadas (Medicina, "
            "Engenharia, Direito, TI/Desenvolvimento, Consultoria, etc.) NÃO "
            "podem ser MEI."
            ""
            "2. **ME (Microempresa):**"
            "- Limite: Até R$ 360.000,00/ano."
            "- Atividades: Todas, incluindo intelectuais e regulamentadas."
            "- Regra de Ouro: Se a atividade for impeditiva para MEI ou o "
            "faturamento for superior a 81k, classifique como ME."
            ""
            "3. **OUTRAS CATEGORIAS**"
            "- Tudo que não se incluir em MEI ou ME."
            ""
            "### LÓGICA DE CNAE:"
            "- Identifique o CNAE principal e até 2 CNAEs secundários se "
            "aplicável."
            "- Verifique se o CNAE sugerido é permitido no regime "
            "MEI (baseado "
            "na Tabela de Atividades Permitidas no MEI)."
            ""
            "### FORMATO DE SAÍDA:"
            "Resposta exclusivamente em JSON, sem blocos de código markdown."
            ""
            "### ESQUEMA DO JSON:"
            "{"
            '"classificacao_pj": "MEI" | "ME" | "Outro",'
            '"setor_atuacao": "Serviços" | "Comércio" | "Indústria",'
            '"perfil_resumo": "string",'
            '"justificativa_enquadramento": "string explicando a escolha '
            'entre MEI/ME",'
            '"cnae_principal": {'
            '"codigo": "0000-0/00",'
            '"descricao": "string",'
            '"permitido_mei": boolean'
            "},"
            '"cnaes_secundarios": ['
            "{"
            '"codigo": "0000-0/00",'
            '"descricao": "string",'
            '"permitido_mei": boolean'
            "}"
            "],"
            '"alerta_impeditivo": "string ou null (ex: \'Atividade de '
            "Engenharia impede MEI')\""
            "}"
        )

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=data),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1,
            max_output_tokens=16000,
            thinking_config=types.ThinkingConfig(
                thinking_budget=0,
            ),
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="BLOCK_LOW_AND_ABOVE",  # Block most
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="BLOCK_LOW_AND_ABOVE",  # Block most
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="BLOCK_LOW_AND_ABOVE",  # Block most
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_LOW_AND_ABOVE",  # Block most
                ),
            ],
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                required=[
                    "classificacao_pj",
                    "setor_atuacao",
                    "perfil_resumo",
                    "justificativa_enquadramento",
                    "cnae_principal",
                    "cnaes_secundarios",
                    "alerta_impeditivo",
                ],
                properties={
                    "classificacao_pj": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        enum=["MEI", "ME", "Outro"],
                    ),
                    "setor_atuacao": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        enum=["Serviços", "Comércio", "Indústria"],
                    ),
                    "perfil_resumo": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                    "justificativa_enquadramento": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                    "cnae_principal": genai.types.Schema(
                        type=genai.types.Type.OBJECT,
                        required=["codigo", "descricao", "permitido_mei"],
                        properties={
                            "codigo": genai.types.Schema(type=genai.types.Type.STRING),
                            "descricao": genai.types.Schema(
                                type=genai.types.Type.STRING
                            ),
                            "permitido_mei": genai.types.Schema(
                                type=genai.types.Type.BOOLEAN
                            ),
                        },
                    ),
                    "cnaes_secundarios": genai.types.Schema(
                        type=genai.types.Type.ARRAY,
                        items=genai.types.Schema(
                            type=genai.types.Type.OBJECT,
                            required=["codigo", "descricao", "permitido_mei"],
                            properties={
                                "codigo": genai.types.Schema(
                                    type=genai.types.Type.STRING
                                ),
                                "descricao": genai.types.Schema(
                                    type=genai.types.Type.STRING
                                ),
                                "permitido_mei": genai.types.Schema(
                                    type=genai.types.Type.BOOLEAN
                                ),
                            },
                        ),
                    ),
                    "alerta_impeditivo": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        nullable=True,
                    ),
                },
            ),
        )

        chunks = []
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            chunks.append(chunk)

        response_data = "".join(chunk.text for chunk in chunks)
        return json.loads(response_data)
