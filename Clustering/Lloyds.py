import random
from typing import List, Tuple

import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt


def k_means(points: np.ndarray, no_of_clusters: int):
    centroids = points[np.random.randint(points.shape[0], size=no_of_clusters)]
    distances = np.zeros([points.shape[0], no_of_clusters], dtype=np.float64)

    previous_distance = -1
    breaking = False
    while True:
        distance_score = 0

        for count, centroid in enumerate(centroids):
            distances[:, count] = np.linalg.norm(points - centroid, axis=1)
        classes = np.argmin(distances, axis=1)
        if breaking:
            break
        for c in range(no_of_clusters):
            centroids[c] = np.mean(points[classes == c], 0)
            print(np.sum(points[classes == c]))
            distance_score += np.sum(points[classes == c])
        if abs(previous_distance - distance_score) < 0.0001:
            breaking = True
        previous_distance = distance_score
    return centroids, classes


def main():
    points, y = make_blobs(centers=[(0, 5), (5, 0), (0, 0), (5, 5)], n_samples=1000,
                           cluster_std=0.5, random_state=1)
    centroids, classes = k_means(points, 4)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.scatter(points[:, 0], points[:, 1], alpha=0.5)
    ax.scatter(centroids[:, 0], centroids[:, 1], marker='o', lw=2)
    ax.set_xlabel('$x_0$')
    ax.set_ylabel('$x_1$')

    plt.show()


if __name__ == '__main__':
    main()
