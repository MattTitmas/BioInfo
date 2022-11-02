from typing import Dict, List

import sklearn
import markov_clustering as mc

import numpy as np


def mcl(G: Dict[str, List[str]], e: int = 2, r: int = 2,
        pruning_threshold: float = 0.001):
    # Initialse M
    M = [[0 for i in range(len(G.keys()))] for i in range(len(G.keys()))]
    for count_one, node_one in enumerate(sorted(G.keys())):
        for count_two, node_two in enumerate(sorted(G.keys())):
            M[count_one][count_two] = 1 if node_two in G[node_one] else 0
        # Allow self loops
        M[count_one][count_one] = 1
    M = np.asarray(M, dtype=np.float64)

    # Values must be in range 0-1, therefore normalise M
    M = sklearn.preprocessing.normalize(M, norm="l1", axis=0)
    while True:
        # Expand
        last = M.copy()
        M = np.linalg.matrix_power(M, e)

        # Inflate
        M = sklearn.preprocessing.normalize(np.power(M, r), norm="l1", axis=0)

        # Prune - not necessary but speeds up (Removes all values < {pruning_threshold}
        pruned = M.copy()
        pruned[pruned < pruning_threshold] = 0
        num_cols = M.shape[1]
        row_indices = M.argmax(axis=0).reshape((num_cols,))
        col_indices = np.arange(num_cols)
        pruned[row_indices, col_indices] = M[row_indices, col_indices]
        M = pruned
        if np.array_equal(last, M):
            # sorted into clusters, now extract the clusters
            keys = sorted(G.keys())
            attractors = M.diagonal().nonzero()[0]
            clusters = []
            for attractor in attractors:
                clusters.append(tuple(keys[i] for i in M[attractor].nonzero()[0].tolist()))
            return clusters


def main():
    graph = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'C', 'D', 'E'],
        'C': ['A', 'B'],
        'D': ['A', 'B', 'I'],
        'E': ['B', 'F', 'G'],
        'F': ['E', 'G'],
        'G': ['F', 'H', 'I'],
        'H': ['G'],
        'I': ['D', 'G', 'J', 'K'],
        'J': ['I', 'K'],
        'K': ['I', 'J']
    }
    print(mcl(graph))


if __name__ == '__main__':
    main()
