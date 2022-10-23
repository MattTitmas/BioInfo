import argparse

from NWA import nwa

# Implementation of Hirschberg's algorithm
# Video providing a visual explanation: https://www.youtube.com/watch?v=cPQeJt-2Y1Q&ab_channel=DavidPowell
# TODO: Why the random reverses?


def nwaScore(string_one: str, string_two: str, verbose: bool = False,
             match: int = 1, mismatch: int = -1, indel: int = -1):
    """
    Caluclate the last row of the matrix produced by NWA, using O(n) space
    :param string_one: The first string
    :param string_two: The second string
    :param verbose: Should the function be verbose
    :param match: Reward for finding a match
    :param mismatch: Penalty for accepting a mismatch
    :param indel: Penalty for accepting an insert / delete
    :return: The last row of the matrix produced by {string_one} and {string_two}
    """

    m = len(string_one)
    n = len(string_two)

    current = [i * indel for i in range(n + 1)]
    next = [0 for i in range(n + 1)]

    for i in range(1, m + 1):
        next[0] = -i
        for j in range(1, n + 1):
            diagonal = current[j-1] + (match if string_two[j - 1] == string_one[i - 1] else mismatch)
            up = current[j] + indel
            left = next[j-1] + indel
            next[j] = max(diagonal, up, left)
        current = next
        next = [0 for i in range(n + 1)]
    return current


def hirschberg(first_string: str, second_string: str, verbose: bool = False, tabs: int = 0):
    if verbose:
        tab_space = "\t" * tabs
        to_print_second = second_string if len(second_string) != 0 else '_'
        to_print_first = first_string if len(first_string) != 0 else '_'
        print(f'{tab_space}Calculating: {to_print_first} and {to_print_second}')
    Z = ""
    W = ""
    if len(first_string) == 0:
        for i in range(0, len(second_string)):
            Z += '-'
            W += second_string[i]
        if verbose:
            tab_space = "\t" * (tabs + 1)
            print(f'{tab_space}Returning: {Z}, {W}')
        return Z, W
    elif len(second_string) == 0:
        for i in range(0, len(first_string)):
            Z += first_string[i]
            W += '-'
        if verbose:
            tab_space = "\t" * (tabs + 1)
            print(f'{tab_space}Returning: {Z}, {W}')
        return Z, W
    elif len(first_string) == 1 or len(second_string) == 1:
        Z, W = nwa(first_string, second_string)
        if verbose:
            tab_space = "\t" * (tabs + 1)
            print(f'{tab_space}Returning: {Z}, {W}')
        return Z, W
    first_string_len = len(first_string)
    first_string_mid = first_string_len//2

    scoreL = nwaScore(first_string[:first_string_mid], second_string)
    scoreR = nwaScore(first_string[first_string_mid:][::-1], second_string[::-1])

    sum_of_scores = [i+j for i, j in zip(scoreL, scoreR[::-1])]
    second_string_mid = max(range(len(sum_of_scores)), key=sum_of_scores.__getitem__)

    Z1, W1 = hirschberg(first_string[:first_string_mid], second_string[:second_string_mid], verbose, tabs + 1)
    Z2, W2 = hirschberg(first_string[first_string_mid:], second_string[second_string_mid:], verbose, tabs + 1)

    if verbose:
        tab_space = "\t" * (tabs + 1)
        print(f'{tab_space}Returning: {Z}, {W}')
    return Z1 + Z2, W1 + W2


def main(first_string: str, second_string: str, verbose: bool = False):
    global_alignment = hirschberg(first_string, second_string, verbose)
    print(f'\nGlobal Alignment of "{first_string}" and "{second_string}": \n'
          f'{global_alignment[0]} & \n{global_alignment[1]}')


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


