import json
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from ferramentas import consultar_catalogo
import streamlit as st

# conectar o LangChain à API do Google Gemini
modelo = ChatOpenAI(
    model="gemini-3.1-flash-lite",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0
)

# interface do usuário
st.title("🚗 Assistente de Autopeças")
st.write("Digite sua dúvida sobre uma peça e eu consultarei o catálogo.")

pergunta = st.text_area("Digite sua pergunta: ", height=120)
st.caption("ℹ️ Máximo de 250 caracteres.")

# preparar guardrail
TERMOS_AUTOPECAS = ["peça","peca","filtro","pastilha","freio","óleo","oleo","motor","vela","bateria","pneu","amortecedor","embreagem","radiador","carro","veículo","veiculo"]

# fazer a LLM entender a pergunta
if st.button("Consultar"):
    if not pergunta:
        st.warning("Digite uma pergunta antes de consultar.")

    elif len(pergunta) > 250:
        st.warning("Sua pergunta é muito longa. Digite uma dúvida com até 250 caracteres.")

    else:
        pergunta_normalizada = pergunta.lower()

        # verificar se o usuário escreveu o ano por extenso
        if re.search(r"\b(?:mil novecentos|dois mil)\b", pergunta_normalizada):
            st.warning(
                "Para evitar interpretações incorretas, informe o ano com quatro dígitos, por exemplo, 2020."
            )
            st.stop()

        # identificar um possível ano informado pelo usuário
        anos_encontrados = re.findall(r"\b\d{4}\b", pergunta)

        # validar o ano original antes de enviar a pergunta para a LLM
        if anos_encontrados:
            ano_informado = int(anos_encontrados[0])

            if ano_informado < 1900 or ano_informado > 2100:
                st.warning("O ano informado está fora de um intervalo válido.")
                st.stop()

        if not any(termo in pergunta_normalizada for termo in TERMOS_AUTOPECAS):
            st.warning("Posso ajudar apenas com consultas sobre autopeças e veículos.")

        else:
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
            try:
                dados = json.loads(conteudo)
            except json.JSONDecodeError:
                st.error(
                    "Não foi possível processar a resposta. "
                    "Tente reformular sua pergunta."
                )
                st.stop()

            # verificar se a resposta é um objeto JSON
            if not isinstance(dados, dict):
                st.error(
                    "Formato inesperado. "
                    "Tente reformular sua pergunta."
                )
                st.stop()

            # verificar se todos os campos esperados estão presentes
            campos_obrigatorios = ["peca", "marca", "modelo", "ano"]

            if not all(campo in dados for campo in campos_obrigatorios):
                st.error(
                    "A IA não conseguiu identificar corretamente os dados da pergunta. "
                    "Tente informar a peça, marca, modelo e ano."
                )
                st.stop()

            # validar se a peça foi identificada
            if not dados["peca"] or not str(dados["peca"]).strip():
                st.warning(
                    "Não consegui identificar qual peça você procura. "
                    "Tente informar o nome da peça."
                )
                st.stop()

            # validar e preservar o ano informado originalmente pelo usuário
            if dados["ano"] is not None:
                try:
                    dados["ano"] = int(dados["ano"])
                except (ValueError, TypeError):
                    st.warning("O ano informado não é válido. Informe um ano numérico.")
                    st.stop()

                if dados["ano"] < 1900 or dados["ano"] > 2100:
                    st.warning("O ano informado está fora de um intervalo válido.")
                    st.stop()

            # se o usuário informou um ano, usar o valor original informado por ele
            if anos_encontrados:
                dados["ano"] = ano_informado

            # executar a Tool do LangChain
            try:
                resultado = consultar_catalogo.invoke({
                    "peca": dados["peca"],
                    "marca": dados["marca"],
                    "modelo": dados["modelo"],
                    "ano": dados["ano"]
                })
            except ValueError as erro:
                st.warning(str(erro))
                st.stop()
            except FileNotFoundError as erro:
                st.error(str(erro))
                st.stop()
            except Exception:
                st.error("Ocorreu um erro ao consultar o catálogo. Tente novamente.")
                st.stop()

            # criar um prompt para transformar o resultado em uma resposta amigável
            prompt_resposta = ChatPromptTemplate.from_template("""
            Você é um atendente de uma loja de autopeças.

            - Responda ao cliente de forma clara, curta e amigável.
            - Responda somente com base na pergunta, nos dados identificados e no resultado da consulta.
            - Não invente horário de funcionamento, endereço, nome da loja, telefone, preços ou qualquer outra informação que não tenha sido fornecida.
            - Se a pergunta estiver fora do escopo de consulta de autopeças, diga que você pode ajudar com consultas de peças do catálogo.

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

            st.subheader("Resposta do assistente:")
            st.write(resposta_final.content)