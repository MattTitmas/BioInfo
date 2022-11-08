from typing import List, Dict


def hamiltonian_path(matrix: Dict[str, Dict[str, int]]):
    n = len(matrix)
    dp = [[False for i in range(1 << n)]
          for j in range(n)]

    # Set all dp[i][(1 << i)] to
    # true
    for count_i, key in enumerate(matrix):
        dp[count_i][1 << count_i] = key

    for i in range(1 << n):
        for count_j, j in enumerate(matrix):
            if (i & (1 << count_j)) != 0:
                for count_k, k in enumerate(matrix):
                    if ((i & (1 << count_k)) != 0 and
                            matrix[k][j] == 1 and
                            j != k and
                            dp[count_k][i ^ (1 << count_j)]):
                        # Update dp[j][i]
                        # to true
                        dp[count_j][i] = k
                        break

    path = set()
    for i, key in enumerate(matrix):

        # Hamiltonian Path exists
        if (dp[i][(1 << n) - 1]):
            path.add(tuple(sorted((key, dp[i][(1 << n) - 1]))))

    if len(path) != n-1:
        return []
    return sorted([i for i in path], key= lambda x: x[1])


def main():
    matrix = {
        'A': {'A': 0, 'B': 1, 'C': 1, 'D': 0, 'E': 0, 'F': 0, 'G': 1, 'H': 1},
        'B': {'A': 1, 'B': 0, 'C': 1, 'D': 0, 'E': 0, 'F': 1, 'G': 0, 'H': 0},
        'C': {'A': 1, 'B': 1, 'C': 0, 'D': 1, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
        'D': {'A': 0, 'B': 0, 'C': 1, 'D': 0, 'E': 1, 'F': 1, 'G': 0, 'H': 0},
        'E': {'A': 0, 'B': 0, 'C': 0, 'D': 1, 'E': 0, 'F': 1, 'G': 0, 'H': 0},
        'F': {'A': 0, 'B': 1, 'C': 0, 'D': 1, 'E': 1, 'F': 0, 'G': 1, 'H': 0},
        'G': {'A': 1, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 1, 'G': 0, 'H': 1},
        'H': {'A': 1, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 1, 'H': 0}
    }

    path = hamiltonian_path(matrix)
    if len(path) == 0:
        print(f'There is no hamiltonian path for the given graph.')
    else:
        print(f'The hamiltonian path for the given matrix can be found by connecting these nodes:\n'
              f'{", ".join([" -> ".join(i) for i in path])}')


if __name__ == '__main__':
    main()
