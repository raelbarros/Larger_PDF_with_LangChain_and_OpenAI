import faiss
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
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
            D_all: Lista de distâncias dos vizinhos mais próximos para cada cluster
            I_all: Lista de índices dos vizinhos mais próximos para cada cluster
            labels: Labels dos clusters para cada ponto
            centroids: Centroids dos clusters
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

        # Cria indice de similaridade por distancia euclidiana L2
        index = faiss.IndexFlatL2(dimension)
        # Adiciona vetor ao indice
        index.add(x)

        # Pega os "centro" do cluster
        centroids = model.centroids
        print("Centroids dos Clusters:")
        print(centroids)

        # Realiza busca para encontrar todos os vizinhos próximos dos centroids
        D_all = []
        I_all = []
        labels = model.index.search(x, 1)[1].reshape(-1)  # labels de cada ponto
        for i, centroid in enumerate(centroids):
            D, I = index.search(np.array([centroid]), num_points)
            D_all.append(D[0])
            I_all.append(I[0])

        return D_all, I_all, labels, centroids


def plot_clusters(x, labels, centroids):
    pca = PCA(n_components=2)
    x_pca = pca.fit_transform(x)
    centroids_pca = pca.transform(centroids)

    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(x_pca[:, 0], x_pca[:, 1], c=labels, cmap='viridis', s=50)
    plt.scatter(centroids_pca[:, 0], centroids_pca[:, 1], c='red', s=200, alpha=0.75, marker='X')
    plt.colorbar(scatter)
    plt.title("Clusters com PCA")
    plt.xlabel("Componente Principal 1")
    plt.ylabel("Componente Principal 2")
    plt.show()

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de dados
    np.random.seed(123)
    x = np.random.random((100, 5)).astype('float32')

    cluster_model = ClusterModel()
    D_all, I_all, labels, centroids = cluster_model.model_kmeans(x, num_cluster=5, num_niter=20)

    # Plotar os clusters
    plot_clusters(x, labels, centroids)
