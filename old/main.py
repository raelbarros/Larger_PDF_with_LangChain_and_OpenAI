import fitz
from pprint import pprint
import asyncio


def read_pdf_in_batches(pdf_path, batch_size=10):
    pdf_document = fitz.open(pdf_path)
    num_pages = pdf_document.page_count

    for i in range(0, 1, batch_size):
        list_page_text = []
        for j in range(i, min(i + batch_size, num_pages)):
            page = pdf_document[j]
            txt = page.get_text()
            list_page_text.append(f"Page {j + 1}:\n{txt}")
        return list_page_text


pdf_path = "./data/1000169-38.2024.8.26.0354.pdf"
test = read_pdf_in_batches(pdf_path)

dados = {
    "custom_id": "request-1",
    "method": "POST",
    "url": "/v1/chat/completions",
    "body": {
        "model": "gpt-3.5-turbo-0125",
        "messages": [
            {
                "role": "system",
                "content": "Você é um assistente útil que responde a perguntas relacionadas a processo de recuperação judicial.",
            },
            {"role": "user", "content": f"{[text for text in test]}"},
            {
                "role": "assistant",
                "content": "a petição de recuperacao judicial identificou as causas concretas da crise economica da empresa?",
            },
            {
                "role": "user",
                "content": "Voce pode me informar o CNPJ da Empresa em Recuperação, o advogado dessa empresa com o seu OAB e as pagina que contem essas importações por favor",
            },
        ],
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 1,
        "n": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    },
}
import json

# Serializando o objeto em uma string JSON
json_str = json.dumps(dados)

# Gravando a string JSON em um arquivo
with open("dados.json", "w") as arquivo:
    arquivo.write(json_str)
