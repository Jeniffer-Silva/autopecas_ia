# importar biblioteca
import csv
import unicodedata

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

# função para consultar o catálogo
def consultar_catalogo(peca=None, marca=None,modelo=None,ano=None):
    # criar lista de resultados
    resultados = []

    # abrrir o CSV
    with open(CAMINHO_CATALOGO, mode="r", encoding="utf-8") as arquivo:
        # função que trata cada linha do CSV como um dicionário
        leitor = csv.DictReader(arquivo)

        # percorrer cada peça
        for item in leitor:
            # verificar se o texto pesquisado está dentro do nome da peça
            if peca and normalizar_texto(peca) not in normalizar_texto(item["peca"]):
                continue

            # verificar se a marca informada é diferente da marca da peça
            if marca and normalizar_texto(marca) != normalizar_texto(item["marca"]):
                continue

            # verificar se o modelo informado é diferente do modelo da peça
            if modelo and normalizar_texto(modelo) != normalizar_texto(item["modelo"]):
                continue

            # se o usuário informar o ano, transformar o ano em inteiro
            if ano:
                ano = int(ano)

                # verificar se o ano pesquisado está dentro do intervalo de compatibilidade da peça
                if not (
                    int(item["ano_inicio"]) <= ano <= int(item["ano_fim"])
                ):
                    continue

            # adicionar o a peça que passou pelas verificações ao final da lista
            resultados.append(item)

    # retornar com as peças encontradas
    return resultados