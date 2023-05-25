import numpy as np

# Not actually sure this works at all, use with lots of caution!
# Will eventually (hopefully) test and fix before exams!


def _prob_sequence(V, A, B, start) -> float:
    if len(V) == 1:
        return B[start][V[0]]
    probability = 0
    for i in range(A.shape[0]):
        probability += _prob_sequence(V[1:], A, B, i) * A[start][i]
    probability *= B[start][V[0]]
    return probability


def prob_sequence(V, A, B, Pi) -> float:
    probability = 0
    for i in range(len(Pi)):
        probability += _prob_sequence(V, A, B, i) * Pi[i]
    return probability


def viterbi(y, A, B, Pi=None):
    # Cardinality of the state space
    K = A.shape[0]
    # Initialize the priors with default (uniform dist) if not given by caller
    Pi = Pi if Pi is not None else np.full(K, 1 / K)
    T = len(y)
    T1 = np.empty((K, T), 'd')
    T2 = np.empty((K, T), 'B')

    # Initilaize the tracking tables from first observation
    T1[:, 0] = Pi * B[:, y[0]]
    T2[:, 0] = 0

    # Iterate throught the observations updating the tracking tables
    for i in range(1, T):
        T1[:, i] = np.max(T1[:, i - 1] * A.T * B[np.newaxis, :, y[i]].T, 1)
        T2[:, i] = np.argmax(T1[:, i - 1] * A.T, 1)

    # Build the output, optimal model trajectory
    x = np.empty(T, 'B')
    x[-1] = np.argmax(T1[:, T - 1])
    for i in reversed(range(1, T)):
        x[i - 1] = T2[x[i], i]

    return x


def forward(V, A, B, Pi=None, steps=-1):
    steps_taken = 0
    K = A.shape[0]
    Pi = Pi if Pi is not None else np.full(K, 1 / K)
    alpha = np.zeros((V.shape[0], A.shape[0]))
    alpha[0, :] = Pi * B[:, V[0]]
    for t in range(1, V.shape[0]):
        steps_taken += 1
        if steps_taken == steps:
            print(steps_taken)
            return alpha[steps_taken - 1]
        for j in range(A.shape[0]):
            # Matrix Computation Steps
            #                  ((1x2) . (1x2))      *     (1)
            #                        (1)            *     (1)
            alpha[t, j] = alpha[t - 1].dot(A[:, j]) * B[j, V[t]]

    return alpha


def translate(observations: str | np.ndarray):
    if type(observations) == str:
        mappings = {
            'A': 0,
            'T': 1,
            'C': 2,
            'G': 3
        }
        return np.array([mappings[i] for i in list(observations)])
    mappings = {
        0: 'x',
        1: 'y',
        2: 'z'
    }
    return ''.join([mappings[i] for i in observations])


def main():
    initial_prob = np.array([0.3, 0.3, 0.4])

    transition_matrix = np.array([
        [0.2, 0.4, 0.4],
        [0.1, 0.6, 0.3],
        [0.8, 0.1, 0.1]
    ])
    emission_matrix = np.array([
        [0.7, 0.1, 0.1, 0.1],
        [0.3, 0.2, 0.4, 0.1],
        [0.4, 0.2, 0.2, 0.2]
    ])

    given_observations = 'CCGAAGTG'
    observations = translate(given_observations)

    path = viterbi(observations, transition_matrix, emission_matrix, initial_prob)

    print(forward(observations, transition_matrix, emission_matrix, initial_prob, 3))


if __name__ == '__main__':
    main()
