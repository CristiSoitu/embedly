import umap
from sklearn.manifold import TSNE


def compute_umap(data, n_components=2, n_neighbors=15, min_dist=0.1, metric='euclidean', random_state=42):
    '''
    Compute UMAP embeddings.

    Args:
        data (numpy.ndarray): Data to embed.
        n_components (int): Number of components.
        n_neighbors (int): Number of neighbors.
        min_dist (float): Minimum distance.
        metric (str): Metric.
        random_state (int): Random state.

    Returns:
        numpy.ndarray: UMAP embeddings.
    '''

    reducer = umap.UMAP(n_components=n_components, n_neighbors=n_neighbors, min_dist=min_dist, metric=metric, random_state=random_state)
    embeddings = reducer.fit_transform(data)

    return embeddings

def compute_tsne(data, n_components=2, perplexity=30, metric='euclidean', random_state=42):
    '''
    Compute t-SNE embeddings.

    Args:
        data (numpy.ndarray): Data to embed.
        n_components (int): Number of components.
        perplexity (int): Perplexity.
        metric (str): Metric.
        random_state (int): Random state.

    Returns:
        numpy.ndarray: t-SNE embeddings.
    '''

    reducer = TSNE(n_components=n_components, perplexity=perplexity, metric=metric, random_state=random_state)
    embeddings = reducer.fit_transform(data)

    return embeddings