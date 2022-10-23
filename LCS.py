import argparse

# Dynamic programming implementation of LCS problem
# Interactive demo: https://www.cs.usfca.edu/~galles/visualization/DPLCS.html


def lcs(string_one: str, string_two: str, verbose: bool = False):
    """
    Calculate the Longest Common Subsequence of two strings
    :param string_one: The first string
    :param string_two: The second string
    :param verbose: Should the function be verbose
    :return: The Longest Common Subsequence of {StringOne} and {StringTwo}
    """

    m = len(string_one)
    n = len(string_two)

    L = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Following steps build L[m+1][n+1] in bottom up fashion. Note
    # that L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1]
    if verbose:
        print(f'Finding the Longest Common Subsequence of {string_one} and {string_two}\n')
        print(f'1. Producing the graph:')

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                # Edges should be 0
                L[i][j] = 0
            elif string_one[i - 1] == string_two[j - 1]:
                # If they are the same, diagonal + 1
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                # If they differ, max of above or left
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    index = L[m][n]

    if verbose:
        print(f'\t       {" ".join([(" " * (len(str(index)) - 1)) + i for i in list(string_two)])}')
        print(f'\t{"-" * (n * (len(str(index)) + 1) + 8)}')
        for col, letter in zip(L, list(' ' + string_one)):
            print(f'\t{letter} | {" ".join([(" " * (len(str(index)) - len(str(i)))) + str(i) for i in col])}')
        print()

    # Following code is used to print LCS

    # Create a character array to store the lcs string
    lcs = [""] * (index + 1)
    lcs[index] = "\0"

    # Start from the right-most-bottom-most corner and
    # one by one store characters in lcs[]
    i = m
    j = n

    if verbose:
        print('2. Navigating the graph (backtracking):')
    while i > 0 and j > 0:
        # If current character in X[] and Y are same, then
        # current character is part of LCS
        if string_one[i - 1] == string_two[j - 1]:
            lcs[index - 1] = string_one[i - 1]
            if verbose:
                print(f'\tAdding {string_one[i - 1]} from position {i, j}')
            i -= 1
            j -= 1
            index -= 1

        # If not same, then find the larger of two and
        # go in the direction of larger value
        elif L[i - 1][j] > L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    if verbose:
        print()

    return "".join(lcs)


def main(first_string: str, second_string: str, verbose: bool = False):
    print(f'Longest Common Subsequence of "{first_string}" and "{second_string}": '
          f'{lcs(first_string, second_string, verbose)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the longest common subsequence of two strings.')
    parser.add_argument('-f', '--first', required=True, type=str,
                        help='First string.')
    parser.add_argument('-s', '--second', required=True, type=str,
                        help='Second string.')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='Verbose output.')
    args = parser.parse_args()

    main(args.first, args.second, args.verbose)


