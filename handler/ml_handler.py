import os
import numpy as np
import openai
import faiss
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from handler.utils import chunk_text
from tqdm import tqdm
from loguru import logger

# FIXME:
os.environ["OPENAI_API_KEY"] = ""


class MLHandler:
    logger.info("Iniciando ML Handler")

    def semantic_split(self, text: str, type="interquartile") -> list:
        """Funcao responsavel por dividir o texto e agrupar com simularidade

        Args:
            text (str): texto a ser dividido.
            type (str, optional): criterio de separacao da frase. Defaults to "interquartile": similaridade semantica.

        Returns:
            list: lista de objetos do tipo "documento" para cada chunk
        """
        logger.info("Realizando divisao por semantica")

        if not isinstance(text, str):
            logger.error("O texto fornecido deve ser uma string")
            raise TypeError("O texto fornecido deve ser uma string")

        text_splitter = SemanticChunker(
            OpenAIEmbeddings(), breakpoint_threshold_type=type
        )

        return text_splitter.create_documents([text])

    def get_embeddings(self, texts: list) -> list:
        """Funcao responsavel por realizar o embedding de cada pedaco de exto

        Args:
            texts (list): Lista de textos que sera convertindo em embedding

        Returns:
            list: Lista contendo os embeddings dos textos fornecidos
        """
        logger.info("Realizando Embedding")

        list_embedding = []

        for text in texts:
            parts = chunk_text(text)

            for part in parts:
                response = openai.embeddings.create(
                    model="text-embedding-3-small", input=part
                )
                list_embedding.append(response.data)

        return list_embedding

    def model_kmeans(self, x, num_cluster=50, num_niter=20):
        """Realiza o modelo de Clusterizacao

        Args:
            array (np.array): Valores a serem utilizados no modelo
            num_cluster (int, optional): Numero de clusters do algoritmo. Defaults to 50.
            niter (int, optional): Numero de interacao do algoritmo. Defaults to 20.

        Returns:
            D: Distancia do vizinho mais proximo
            I: Indice do vizinho mais proximo
        """
        logger.info("Iniciando Clusterizacao")

        dimension = x.shape[1]  # dimensao  do vetor
        num_points = x.shape[0]  # qtd de linhas do vetor

        # Verificar se o numero de linhas e suficiente para o numero de clusters
        if num_points < num_cluster:
            num_cluster = num_points
            logger.info(
                f"Numero de clusters ajustado para {num_cluster} devido ao numero insuficiente de pontos de dados."
            )

        logger.info("Treinando o modelo")
        model = faiss.Kmeans(dimension, num_cluster, niter=num_niter, verbose=True)
        model.train(x)

        # Cria indice de simularidade por distancia euclidiana L2
        index = faiss.IndexFlatL2(dimension)
        # Add vetor ao indice
        index.add(x)

        # Pega os "centro" do cluster
        centroids = model.centroids

        # Realiza busta nos centroids para encontrar o vizinho mais proxim
        D, I = index.search(centroids, 1)  # acessando o vetor mais proximo do centro
        return D, I
    

    def ask_gpt(self, user_prompt, pdf_doc, gpt_model="gpt-4"):
        """Realiza perguntas para o GPT com os resumos do PDF

        Args:
            user_message (str): Mensagem de prompt do usuario
            pdf_doc (list): Lista de objetos "Documentos" para serem usados no GPT
            gpt_model (str): engine do modelo do GPT

        Returns:
            final_resp: Resposta do GPT
        """
        logger.info("Iniciando pergunta para o GPT")

        logger.info(f"GPT Engine: {gpt_model}")
        model = ChatOpenAI(temperature=0, model=gpt_model)

        logger.info("Montando a mensagem")
        
        msg = """
            {user_message}

            ```{text}```
            SUMMARY:
        """

        prompt = ChatPromptTemplate.from_template(msg)

        # Define a cademia de processamento
        # prepara msg, manda para o modelo e passa a resposta para o StrOutputParser
        chain = ( prompt | model | StrOutputParser() )

        final_resp = ""

        # Intera em cada documento do PDF
        for doc in tqdm(pdf_doc, desc="Processando textos no GPT"):
            # Divide os documentos em partes
            parts = chunk_text(doc.page_content)

            # Intera cada part na cadeia
            for part in parts:
                resp = chain.invoke({"user_message": user_prompt, "text": part})
                final_resp += f" {resp}"

        return final_resp