from openai import OpenAI
import json
from ferramentas import consultar_catalogo

# conectar ao servidor local do LM Studio
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# elaborar pergunta para a IA
pergunta = "Tem parafuso de motor para Onix 2020?"

# elaborar instrução para a IA 
prompt = f"""
Você é um assistente de uma loja de autopeças.

Sua tarefa é analisar a pergunta do cliente e identificar informações sobre
a PEÇA e sobre o VEÍCULO.

Retorne SOMENTE um objeto JSON válido.
NÃO use blocos de código Markdown.
NÃO escreva ```json.
NÃO escreva qualquer texto antes ou depois do JSON.

Use exatamente estas chaves:

- "peca": nome da peça que o cliente procura
- "marca": marca do veículo
- "modelo": modelo do veículo
- "ano": ano do veículo

Se alguma informação não estiver presente na pergunta, use null.

Exemplo:
Pergunta: "Tem filtro de oleo para Chevrolet Onix 2020?"

Resposta:
{{
    "peca": "filtro de oleo",
    "marca": "Chevrolet",
    "modelo": "Onix",
    "ano": 2020
}}

Agora analise esta pergunta:

{pergunta}
"""

# estruturar chamada para a IA
resposta = client.chat.completions.create(
    model="google/gemma-3-1b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    # obter respostas mais consistentes e menos criativas
    temperature=0
)

# remover espaços e quebras de linha desnecessárias no começo e no fim
conteudo = resposta.choices[0].message.content.strip()

# se a resposta começar com ```json, remover essa parte do início e do final
if conteudo.startswith("```json"):
    conteudo = conteudo.removeprefix("```json").removesuffix("```").strip()

# transformar o texto em um dicionário Python
dados = json.loads(conteudo)

# converter string que vem da IA em int
if dados["ano"] is not None:
    dados["ano"] = int(dados["ano"])

# acessar função
resultado = consultar_catalogo(
    peca=dados["peca"],
    marca=dados["marca"],
    modelo=dados["modelo"],
    ano=dados["ano"]
)

print(resultado)