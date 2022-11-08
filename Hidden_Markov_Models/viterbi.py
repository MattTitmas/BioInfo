from typing import List, Dict


def viterbi(observations: List[str],
            states: List[str],
            initial_prob: Dict[str, float],
            transition_matrix: Dict[str, Dict[str, float]],
            emission_matrix: Dict[str, Dict[str, float]],
            given_observations: List[str]) -> List[str]:

    t_one = [[0.0 for i in range(len(given_observations))] for j in range(len(states))]
    t_two = [[0 for i in range(len(given_observations))] for j in range(len(states))]

    for count, state in enumerate(states):
        t_one[count][0] = initial_prob[state] * emission_matrix[state][given_observations[0]]

    for j, observation in enumerate(given_observations):
        if j == 0:
            continue
        for i, state in enumerate(states):
            values = [t_one[count][j-1] * transition_matrix[k][state] * emission_matrix[state][observation]
                      for count, k in enumerate(states)]
            t_one[i][j] = max(values)
            t_two[i][j] = max(range(len(values)), key=values.__getitem__)

    z = [0 for i in range(len(given_observations))]
    X = ['' for i in range(len(given_observations))]

    values = [t_one[count][len(given_observations)-1] for count, k in enumerate(states)]
    z[len(given_observations)-1] = max(range(len(values)), key=values.__getitem__)
    X[len(given_observations)-1] = states[z[len(given_observations)-1]]

    for j in range(len(given_observations)-1, 0, -1):
        z[j-1] = t_two[z[j]][j]
        X[j-1] = states[z[j-1]]

    return ''.join(X)


def main():
    observations = ['A', 'T', 'C', 'G']
    states = ['x', 'y', 'z']
    initial_prob = {
        'x': 0.3,
        'y': 0.3,
        'z': 0.4
    }
    transition_matrix = {
        'x': {'x': 0.2, 'y': 0.4, 'z': 0.4},
        'y': {'x': 0.1, 'y': 0.6, 'z': 0.3},
        'z': {'x': 0.8, 'y': 0.1, 'z': 0.1}

    }
    emission_matrix = {
        'x': {'A': 0.7, 'T': 0.1, 'C': 0.1, 'G': 0.1},
        'y': {'A': 0.3, 'T': 0.2, 'C': 0.4, 'G': 0.1},
        'z': {'A': 0.4, 'T': 0.2, 'C': 0.2, 'G': 0.2},
    }
    given_observations = 'CCGAAGTG'
    returned_value = viterbi(observations, states, initial_prob, transition_matrix, emission_matrix, given_observations)
    print(returned_value)

if __name__ == '__main__':
    main()
