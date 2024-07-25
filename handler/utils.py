import re
import os


def concat_pages_to_text(doc: list) -> str:
    """Funcao auxiliar para juntar os textos de todas as paginas em uma string,

    Args:
        doc (list): Lista de paginas do documento

    Returns:
        str: string unica contendo os textos do documento.
    """

    return " ".join([page.page_content.replace("\t", " ") for page in doc])  # junta as paginas e remove as tabulacoes


def clear_text(text: str) -> str:
    """Funcao responsavel limpar e formatar um texto de entrada.

    Args:
        text (str): texto de entrada que sera formatado

    Returns:
        str: texto de entrada apos passar por limpeza
    """
    cleaned_text = re.sub(r" +", " ", text)  # remove multiplos espacos
    cleaned_text = re.sub(r"\s*-\s*", "", cleaned_text)  # remove espaco ao redor do hifen
    cleaned_text = cleaned_text.replace("\n", " ")  # remove quebra de linha

    return cleaned_text


def chunk_text(text: str, size=8192) -> list:
    """Funcao responsavel por dividir o texto em partes menores.
        Isso é feito para evitar o limite de tokens da API.

    Args:
        text (str): Texto que sera dividido
        size (int, optional): tamanho de caracteres de divisao. Defaults to 8192.

    Returns:
        list: lista contendo o texto fornecido dividido
    """

    # range(0, len(text), 8192): Gera uma sequencia de 0 ate o tamanho do texto com passos de 8192
    # text[i:i + 8192]: Pega uma fatia do texto do indice i até i + 8192
    return [text[i : i + size] for i in range(0, len(text), size)]
