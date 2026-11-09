import os, json
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

def _client():
    return OpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"))

SYSTEM = ("Voce e um assistente de apoio a recrutamento. Analise o curriculo frente a vaga de forma objetiva, "
          "usando SOMENTE informacoes presentes no texto. Nao invente dados. Ignore nome, genero, idade, foto, "
          "estado civil e nacionalidade. Responda APENAS com JSON valido.")

EXEMPLO = """Exemplo (few-shot):
Vaga: Analista de dados Python e SQL.
Curriculo: 3 anos com Python, pandas e SQL em varejo; dashboards em Power BI.
Saida: {"resumo":"Analista de dados com 3 anos em varejo.","habilidades":["Python","pandas","SQL","Power BI"],
"anos_experiencia":3,"nota_aderencia":85,"pontos_fortes":["Python e SQL exigidos pela vaga"],
"lacunas":["Sem citacao de cloud"],"justificativa":"Cobre os requisitos principais; falta cloud.",
"perguntas_entrevista":["Como validou a qualidade dos dados no varejo?"]}"""

def analisar(curriculo: str, vaga: str, area_prevista: str, confianca: float) -> dict:
    prompt = f"""{EXEMPLO}

Agora analise:
Area prevista pelo modelo de ML: {area_prevista} (confianca {confianca:.0%})
Vaga: {vaga}
Curriculo: {curriculo[:6000]}

Retorne JSON com as chaves: resumo, habilidades, anos_experiencia, nota_aderencia (0-100),
pontos_fortes, lacunas, justificativa, perguntas_entrevista."""
    r = _client().chat.completions.create(
        model=os.getenv("LLM_MODEL"), temperature=0.2,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}])
    txt = r.choices[0].message.content.strip().strip("`")
    if txt.lower().startswith("json"): txt = txt[4:]
    return json.loads(txt[txt.find("{"): txt.rfind("}") + 1])
