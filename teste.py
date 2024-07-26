import faiss
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ClusterModel:
    def model_kmeans(self, x, num_cluster=2, num_niter=20):
        """Realiza o modelo de Clusterizacao

        Args:
            x (np.array): Valores a serem utilizados no modelo
            num_cluster (int, optional): Numero de clusters do algoritmo. Defaults to 50.
            num_niter (int, optional): Numero de iteracao do algoritmo. Defaults to 20.

        Returns:
            D: Distancia dos vizinhos mais proximos
            I: Indices dos vizinhos mais proximos
        """
        logger.info("Iniciando Clusterizacao")

        dimension = x.shape[1]  # dimensao  do vetor
        num_points = x.shape[0]  # qtd de linhas do vetor

        # Verificar se o numero de linhas e suficiente para o numero de clusters
        # if num_points < num_cluster:
        #     num_cluster = num_points
        #     logger.info(
        #         f"Numero de clusters ajustado para {num_cluster} devido ao numero insuficiente de pontos de dados."
        #     )

        logger.info("Treinando o modelo")
        model = faiss.Kmeans(dimension, num_cluster, niter=num_niter, verbose=True)
        model.train(x)

        # Cria indice de similaridade por distancia euclidiana L2
        index = faiss.IndexFlatL2(dimension)
        # Adiciona vetor ao indice
        index.add(x)

        # Pega os "centro" do cluster
        centroids = model.centroids

        # Realiza busta nos centroids para encontrar o vizinho mais proxim
        D, I = index.search(centroids)  # acessando o vetor mais proximo do centro
        return D, I

def model_kmeans(x):
    from sklearn.cluster import KMeans

    model = KMeans(5).fit(x)
    print(model.labels_)
    

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de dados
    np.random.seed(123)
    x = np.random.random((10000, 10)).astype('float32')

    cluster_model = ClusterModel()
    D_all, I_all = cluster_model.model_kmeans(x)
    print(I_all)
    # # Exibir o número de clusters e o número de pontos em cada cluster
    # print(f"Número de clusters: {len(I_all)}")
    # for cluster_idx, indices in enumerate(I_all):
    #     print(f"Cluster {cluster_idx}: {(indices)} pontos")