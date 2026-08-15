# importar biblioteca
import csv
import unicodedata
from langchain.tools import tool

# função para deixar o texto em minúscula e sem acentos
def normalizar_texto(texto):
    texto = texto.lower()
    
    # NFD é uma forma de decomposição Unicode que separa em "letra base + marca de acento"
    texto = unicodedata.normalize("NFD", texto)

    # pegar os caracteres do texto, descartar os que forem marcas Unicode Mn e junte todos os restantes
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    return texto

# guardar o nome do arquivo a ser consultado
CAMINHO_CATALOGO = "catalogo_pecas.csv"

# função para consultar o catálogo transformada em tool para o LangChain
@tool
def consultar_catalogo(peca=None, marca=None, modelo=None, ano=None):
    """Consulta o catálogo de autopeças por peça, marca, modelo e ano."""

    # validar o ano antes de consultar o catálogo
    if ano is not None:
        try:
            ano = int(ano)
        except (ValueError, TypeError):
            raise ValueError("O ano informado deve ser numérico.")

        if ano < 1900 or ano > 2100:
            raise ValueError("O ano informado está fora de um intervalo válido.")

    # criar lista de resultados
    resultados = []

    try:
        # abrir o CSV
        with open(CAMINHO_CATALOGO, mode="r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)

            # percorrer cada peça
            for item in leitor:

                # verificar se o texto pesquisado está dentro do nome da peça
                if peca and normalizar_texto(peca) not in normalizar_texto(item["peca"]):
                    continue

                # verificar a marca
                if marca and normalizar_texto(marca) != normalizar_texto(item["marca"]):
                    continue

                # verificar o modelo
                if modelo and normalizar_texto(modelo) != normalizar_texto(item["modelo"]):
                    continue

                # verificar o ano
                if ano is not None:
                    if not (
                        int(item["ano_inicio"]) <= ano <= int(item["ano_fim"])
                    ):
                        continue

                # adicionar o item encontrado
                resultados.append(item)

    except FileNotFoundError:
        raise FileNotFoundError(
            "O arquivo catalogo_pecas.csv não foi encontrado."
        )

    except (KeyError, ValueError):
        raise ValueError(
            "O catálogo possui dados inválidos ou está em formato inesperado."
        )

    return resultados