import argparse
import re
from typing import Dict, Tuple, List


# Implementation of UPGMA

def combinations(first: str, second: str) -> List[Tuple]:
    first_list = re.findall('[a-zA-Z]+', first)
    second_list = re.findall('[a-zA-Z]+', second)

    to_return = []
    for i in first_list:
        for j in second_list:
            to_return.append((i, j))
    return to_return


def UPGMA(distance_matrix: Dict[str, Dict[str, float]]):
    distance_copy = {i: {j: v_ for j, v_ in v.items()} for i, v in distance_matrix.items()}
    distances = {key: 0 for key in distance_matrix}

    while len(distance_matrix.keys()) >= 2:
        current_minimum, minimum_score = None, float('inf')
        for i in distance_matrix:
            for j in distance_matrix:
                if i == j:
                    continue
                if distance_matrix[i][j] < minimum_score:
                    minimum_score = distance_matrix[i][j]
                    current_minimum = (i, j)
        new_node_name = f'({current_minimum[0]}, {current_minimum[1]})'
        distances[new_node_name] = minimum_score / 2

        new_dict = dict()
        for i in distance_matrix:
            if i in current_minimum:
                continue
            total, length = 0, 0
            print(new_node_name, i)
            for combination in combinations(new_node_name, i):
                total += distance_copy[combination[0]][combination[1]]
                length += 1
            distance_matrix[i].pop(current_minimum[0])
            distance_matrix[i].pop(current_minimum[1])
            distance_matrix[i][new_node_name] = total / length
            new_dict[i] = total / length
        distance_matrix[new_node_name] = {**new_dict, **{new_node_name: 0}}
        distance_matrix.pop(current_minimum[0])
        distance_matrix.pop(current_minimum[1])
        # print('-=-=-=-=-=-=-=-')
        # for key in distance_matrix:
        #     print(f'{key}: {distance_matrix[key]}')
        # input()
    return distances

def main(matrix: str = 'default'):
    if matrix == 'default':
        distance_matrix = {
            'a': {'a': 0 , 'b': 19, 'c': 27, 'd': 8 , 'e': 33, 'f': 18, 'g': 13},
            'b': {'a': 19, 'b': 0 , 'c': 31, 'd': 18, 'e': 36, 'f': 1 , 'g': 13},
            'c': {'a': 27, 'b': 31, 'c': 0 , 'd': 26, 'e': 41, 'f': 32, 'g': 29},
            'd': {'a': 8 , 'b': 18, 'c': 26, 'd': 0 , 'e': 31, 'f': 17, 'g': 14},
            'e': {'a': 33, 'b': 36, 'c': 41, 'd': 31, 'e': 0 , 'f': 35, 'g': 28},
            'f': {'a': 18, 'b': 1 , 'c': 32, 'd': 17, 'e': 35, 'f': 0 , 'g': 12},
            'g': {'a': 13, 'b': 13, 'c': 29, 'd': 14, 'e': 28, 'f': 12, 'g': 0 }
        }
    else:
        distance_matrix = {
            'A': {'A': 0, 'B': 2, 'C': 4, 'D': 6},
            'B': {'A': 2, 'B': 0, 'C': 4, 'D': 6},
            'C': {'A': 4, 'B': 4, 'C': 0, 'D': 6},
            'D': {'A': 6, 'B': 6, 'C': 6, 'D': 0}
        }
    print(UPGMA(distance_matrix))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform UPGMA on a distance matrix.')
    args = parser.parse_args()
    main('s')
