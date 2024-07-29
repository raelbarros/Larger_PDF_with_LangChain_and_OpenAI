from handler.pdf_handler import PDFHandler
from handler.ml_handler import MLHandler
from handler.utils import concat_pages_to_text, clear_text
from loguru import logger
import pandas as pd
import numpy as np


# Iniciando handler de PDF
pdf_handler = PDFHandler()

# Iniciando leitura do PDF
pdf_in_path = './data/input/pdf_sample.pdf'
pdf_doc = pdf_handler.read_pdf(pdf_in_path)

# Convertendo paginas em string
text_doc = concat_pages_to_text(pdf_doc)

# Limpando string
text_cleaned = clear_text(text_doc)

# Iniciando handler de ML
ml_handler = MLHandler()

# Realizando split por semantica
semantic_docs = ml_handler.semantic_split(text_cleaned)

# Realizando embedding do texto
list_embedding = ml_handler.get_embeddings([doc.page_content for doc in semantic_docs])

# Organizando os dados.
logger.info("Organizando os dados")

# TODO: DF para tratamento dos dados
# # Cria df com os dados semanticos e os dados de embedding para facilidar a manipulacao dos dados
# list_content_page = [doc.page_content for doc in semantic_docs]
# df = pd.DataFrame(list_content_page, columns=['page_content'])

#list_vector_embedding = [embedding[0].embedding for embedding in list_embedding]
# df['embeddings'] = list_vector_embedding

# print(df.head())

# Executando o modelo de clusterizacao
list_vector_embedding = [embedding[0].embedding for embedding in list_embedding]
array_embedding = np.array(list_vector_embedding)

_, near_doc_index = ml_handler.model_kmeans(array_embedding)

# Organizadao e processamento dos documentos
# Ordenazao do array de indices
sorted_array = np.sort(near_doc_index, axis=0)
# Muda dimensao
sorted_array = sorted_array.flatten()

# agrupamento dos documentos por cluster
organized_docs = [semantic_docs[i] for i in sorted_array]

# Obtendo resumo de cada documento.
user_prompt = """
    Me explique esse documento por favor
"""
final_text = ml_handler.ask_gpt(user_prompt, organized_docs)

logger.debug(f"Resposta: {final_text}")

pdf_out_path = 'resposta_gpt.pdf'
pdf_handler.create_pdf(final_text, pdf_out_path)

logger.success("Processo finalizado!")
