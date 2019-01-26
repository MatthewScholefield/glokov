from sklearn.cluster import KMeans
import numpy as np


def cluster_points(points: list, n: int) -> KMeans:
    points = np.array(points)
    kmeans = KMeans(n)
    kmeans.fit(points)
    return kmeans
