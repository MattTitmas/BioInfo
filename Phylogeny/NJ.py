from typing import Dict


def neighbour_joining(distance_matrix: Dict[str, Dict[str, float]]):
    limb_length = dict()
    new_node_number = 0
    while len(distance_matrix) > 2:
        total_distance = {i: sum(v.values()) for i, v in distance_matrix.items()}

        distance_star = {i: {j: ((len(total_distance) - 2) * distance_matrix[i][j])
                                - total_distance[i]
                                - total_distance[j] if i != j else 0 for j, v_ in total_distance.items()}
                         for i, v in total_distance.items()}

        minimum_score, current_minimum = 0, None
        for i in distance_star:
            for j in distance_star:
                if i == j:
                    continue
                if distance_star[i][j] < minimum_score:
                    minimum_score = distance_star[i][j]
                    current_minimum = (i, j)

        new_node_name = f'node_{new_node_number}'
        new_node_number += 1
        delta = (total_distance[current_minimum[0]] - total_distance[current_minimum[1]]) / (len(distance_matrix) - 2)
        limb_length[current_minimum[0]] = {
            new_node_name: (1 / 2) * (distance_matrix[current_minimum[0]][current_minimum[1]] + delta)}
        limb_length[current_minimum[1]] = {
            new_node_name: (1 / 2) * (distance_matrix[current_minimum[0]][current_minimum[1]] - delta)}

        existing_keys = list(distance_matrix.keys())

        new_dict = dict()
        for key in existing_keys:
            distance_key_new_node = (distance_matrix[current_minimum[0]][key]
                                     + distance_matrix[current_minimum[1]][key]
                                     - distance_matrix[current_minimum[0]][current_minimum[1]]) / 2
            distance_matrix[key][new_node_name] = distance_key_new_node
            new_dict[key] = distance_key_new_node
        distance_matrix[new_node_name] = {**new_dict, **{new_node_name: 0}}

        for key in distance_matrix:
            distance_matrix[key].pop(current_minimum[0])
            distance_matrix[key].pop(current_minimum[1])
        distance_matrix.pop(current_minimum[0])
        distance_matrix.pop(current_minimum[1])

    keys = list(distance_matrix.keys())
    return {**limb_length, **{keys[0]: {keys[1]: distance_matrix[keys[0]][keys[1]]}}}


def main():
    additive_matrix = {
        'a': {'a': 0, 'b': 5, 'c': 9, 'd': 9, 'e': 8},
        'b': {'a': 5, 'b': 0, 'c': 10, 'd': 10, 'e': 9},
        'c': {'a': 9, 'b': 10, 'c': 0, 'd': 8, 'e': 7},
        'd': {'a': 9, 'b': 10, 'c': 8, 'd': 0, 'e': 3},
        'e': {'a': 8, 'b': 9, 'c': 7, 'd': 3, 'e': 0}
    }
    print(neighbour_joining(additive_matrix))


if __name__ == '__main__':
    main()
