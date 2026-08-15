import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from ferramentas import consultar_catalogo
import streamlit as st

# conectar o LangChain ao servidor local do LM Studio
modelo = ChatOpenAI(
    model="google/gemma-3-1b",
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    temperature=0
)

# interface do usuário
st.title("🚗 Assistente de Autopeças")
st.write("Digite sua dúvida sobre uma peça e eu consultarei o catálogo.")

pergunta = st.text_input("Digite sua pergunta: ")

# fazer a LLM entender a pergunta
if st.button("Consultar"):
    if pergunta:
        # criar o prompt usando LangChain
        prompt = ChatPromptTemplate.from_template("""
        Você é um assistente de uma loja de autopeças.
        Analise a pergunta do cliente e identifique:
        - "peca": nome da peça que o cliente procura
        - "marca": marca do veículo
        - "modelo": modelo do veículo
        - "ano": ano do veículo
        Retorne SOMENTE um objeto JSON válido.
        Não escreva texto antes ou depois do JSON.
        Se uma informação não estiver presente, use null.
        Exemplo:
        Pergunta:
        "Tem filtro de oleo para Chevrolet Onix 2020?"
        Resposta:
        {{
            "peca": "filtro de oleo",
            "marca": "Chevrolet",
            "modelo": "Onix",
            "ano": 2020
        }}
        Pergunta do cliente:
        {pergunta}
        """)

        # executar o prompt + modelo
        resposta = modelo.invoke(
            prompt.format_messages(pergunta=pergunta)
        )

        # pegar o texto produzido pela IA
        conteudo = resposta.content.strip()

        # remover eventual bloco Markdown
        if conteudo.startswith("```json"):
            conteudo = conteudo.removeprefix("```json").removesuffix("```").strip()

        # transformar o JSON em dicionário Python
        dados = json.loads(conteudo)

        # converter o ano para inteiro
        if dados["ano"] is not None:
            dados["ano"] = int(dados["ano"])

        # executar a Tool do LangChain
        resultado = consultar_catalogo.invoke({
            "peca": dados["peca"],
            "marca": dados["marca"],
            "modelo": dados["modelo"],
            "ano": dados["ano"]
        })

        # criar um prompt para transformar o resultado em uma resposta amigável
        prompt_resposta = ChatPromptTemplate.from_template("""
        Você é um atendente de uma loja de autopeças.

        Responda ao cliente de forma clara, curta e amigável.

        Pergunta do cliente:
        {pergunta}

        Dados identificados:
        {dados}

        Resultado da consulta ao catálogo:
        {resultado}

        Regras:
        - Se houver peças encontradas, informe a peça, veículo, aplicação, preço e estoque.
        - Se não houver peças encontradas, diga claramente que não encontrou a peça no catálogo.
        - Não invente informações.
        - Não mencione JSON, Python, LangChain, Tool ou catálogo como estrutura técnica.
        """)

        resposta_final = modelo.invoke(
            prompt_resposta.format_messages(
                pergunta=pergunta,
                dados=dados,
                resultado=resultado
            )
        )

        st.subheader("🤖 Resposta do assistente:")
        st.write(resposta_final.content)

    else:
        st.warning("Digite uma pergunta antes de consultar.")

