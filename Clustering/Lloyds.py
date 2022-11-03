import random
import argparse
from typing import List, Tuple
from functools import partial

import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt


def coords(s):
    try:
        x, y = map(float, s.split(','))
        return x, y
    except:
        raise argparse.ArgumentTypeError("Coordinates must be x,y")

def compute_label(centroids, x):
    return np.argmin(np.sqrt(np.sum((centroids - x)**2, axis=1)))

def k_means(points: np.ndarray, no_of_clusters: int, verbose: bool = False):
    centroids = points[np.random.choice(len(points), no_of_clusters, replace=False)]
    distances = np.zeros([points.shape[0], no_of_clusters], dtype=np.float64)

    prev_label, labels = None, np.zeros(len(points))
    iteration = 0
    while not np.all(labels == prev_label):
        if verbose:
            print(f'Centroid positions at iteration {iteration}:\n {centroids}')
        iteration += 1

        prev_label = labels
        partial_function = partial(compute_label, centroids)
        labels = np.apply_along_axis(partial_function, 1, points)
        centroids = np.array([np.mean(points[labels == k], axis=0) for k in range(no_of_clusters)])
    return centroids, labels


def main(centers: Tuple[Tuple[float, float]] = ((0, 5), (5, 0), (0, 0), (5, 5)),
         number_of_clusters: int = 4,
         verbose: bool = False):
    print()
    points, y = make_blobs(centers=list(centers), n_samples=1000,
                           cluster_std=0.5, random_state=1)
    centroids, classes = k_means(points, number_of_clusters, verbose=verbose)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.scatter(points[:, 0], points[:, 1], alpha=0.5)
    ax.scatter(centroids[:, 0], centroids[:, 1], marker='o', lw=2)
    ax.set_xlabel('$x_0$')
    ax.set_ylabel('$x_1$')

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform LLoyd's algorithm.")
    parser.add_argument('-c', '--centers', type=coords, nargs='+', required=True,
                        help='Center of clusters.')
    parser.add_argument('-n', '--number', type=int, required=True,
                        help='Number of clusters.')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='Verbose output.')
    args = parser.parse_args()
    main(centers=args.centers, number_of_clusters=args.number, verbose=args.verbose)
