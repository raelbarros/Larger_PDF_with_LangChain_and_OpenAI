import streamlit as st
from handler.pdf_handler import PDFHandler
from handler.ml_handler import MLHandler
from handler.utils import concat_pages_to_text, clear_text
from loguru import logger
import numpy as np
import os


def process_pdf(pdf_path, file_name, user_prompt):
    # Iniciando handler de PDF
    pdf_handler = PDFHandler()

    # Iniciando leitura do PDF
    pdf_doc = pdf_handler.read_pdf(pdf_path)
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
    final_text = ml_handler.ask_gpt(user_prompt, organized_docs)

    logger.debug(f"Resposta: {final_text}")

    output_pdf_path = os.path.join("./data/output", f"result_{file_name}")
    pdf_handler.create_pdf(final_text, output_pdf_path)

    return output_pdf_path


def main():
    st.title("Processador de PDFs RJ")

    uploaded_file = st.file_uploader("Carregar arquivo PDF", type="pdf")
    user_prompt = st.text_area("Digite o texto para análise", placeholder='Mensagem do GPT')

    if uploaded_file is not None and user_prompt:
        with st.spinner("Processando..."):
            # Salvar o arquivo carregado
            file_path = os.path.join("./data/input", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Processar o PDF e obter o resultado
            result_pdf_path = process_pdf(file_path, uploaded_file.name, user_prompt)

            # Exibir o resultado
            st.write("Resultado da análise:")

            print(result_pdf_path)
            # Disponibilizar o download do arquivo PDF resultante
            with open(result_pdf_path, "rb") as f:
                st.download_button(
                    label="Baixar resultado em PDF",
                    data=f,
                    file_name=f"result_{uploaded_file.name}",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()
