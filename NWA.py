import argparse


# Dynamic programming implementation of Needleman-Wunsch Alignment
# Interactive demo: https://bioboot.github.io/bimm143_W20/class-material/nw/


def nwa(string_one: str, string_two: str, verbose: bool = False, overlap_detection: bool = False,
        match: int = 1, mismatch: int = -1, indel: int = -1):
    """
    Calculate the global alignments of two strings
    :param string_one: The first string
    :param string_two: The second string
    :param verbose: Should the function be verbose
    :param overlap_detection: Whether to use the overlap detection variant
    :param match: Reward for finding a match
    :param mismatch: Penalty for accepting a mismatch
    :param indel: Penalty for accepting an insert / delete
    :return: The global alignment of {StringOne} and {StringTwo}
    """

    m = len(string_one)
    n = len(string_two)

    score_matrix = [[0 for x in range(n + 1)] for x in range(m + 1)]
    backtrace = [[' ' for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m + 1):
        score_matrix[i][0] = (indel * i) if not overlap_detection else 0
        backtrace[i][0] = 'U'
    for j in range(n + 1):
        score_matrix[0][j] = (indel * j) if not overlap_detection else 0
        backtrace[0][j] = 'L'
    backtrace[0][0] = ' '

    # Following steps build score_matrix[m+1][n+1] in bottom up fashion. Note
    # that score_matrix[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1]
    if verbose:
        print(f'Finding the Longest Common Subsequence of {string_one} and {string_two}\n')
        print(f'1. Producing the graph:')

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diagonal = score_matrix[i - 1][j - 1] + (match if string_one[i - 1] == string_two[j - 1] else mismatch)
            up = score_matrix[i - 1][j] + indel
            left = score_matrix[i][j - 1] + indel

            if diagonal >= left and diagonal >= up:
                score_matrix[i][j] = diagonal
                backtrace[i][j] = 'D'
            elif up >= diagonal and up >= left:
                score_matrix[i][j] = up
                backtrace[i][j] = 'U'
            else:
                score_matrix[i][j] = left
                backtrace[i][j] = 'L'

    index = score_matrix[m][n]

    if verbose:
        print(f'\t       {" ".join([(" " * (len(str(index)))) + i for i in list(string_two)])}')
        print(f'\t{"-" * (n * (len(str(index)) + 2) + 6)}')
        for col, letter in zip(score_matrix, list(' ' + string_one)):
            print(f'\t{letter} | {" ".join([(" " * (len(str(index)) + 1 - len(str(i)))) + str(i) for i in col])}')
        print()

        print(f'\t       {" ".join([(" " * (len(str(index)))) + i for i in list(string_two)])}')
        print(f'\t{"-" * (n * (len(str(index)) + 2) + 6)}')
        for col, letter in zip(backtrace, list(' ' + string_one)):
            print(f'\t{letter} | {" ".join([(" " * (len(str(index)) + 1 - len(str(i)))) + str(i) for i in col])}')
        print()

    to_return_one = ""
    to_return_two = ""

    if verbose:
        print('2. Navigating the graph (backtracking):')
    i, j = m + 1, n + 1
    while i > 1 or j > 1:
        current = backtrace[i - 1][j - 1]
        if current == 'D':
            i -= 1
            j -= 1
            to_return_one = string_one[i - 1] + to_return_one
            to_return_two = string_two[j - 1] + to_return_two
        elif current == 'L':
            j -= 1
            to_return_one = '-' + to_return_one
            to_return_two = string_two[j - 1] + to_return_two
        else:
            i -= 1
            to_return_one = string_one[i - 1] + to_return_one
            to_return_two = '-' + to_return_two
        if verbose:
            print(f'\tMoving {current}, Updating strings:\n\t\t{to_return_one}\n\t\t{to_return_two}')

    return to_return_one, to_return_two


def main(first_string: str, second_string: str, verbose: bool = False,
         indel: int = -1, mismatch: int = -1, match: int = 1,
         overlap_detection: bool = False):
    global_alignment = nwa(first_string, second_string, verbose, overlap_detection,
                           match, mismatch, indel)
    print(f'Global Alignment of "{first_string}" and "{second_string}": \n'
          f'{global_alignment[0]} & \n{global_alignment[1]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the longest common subsequence of two strings.')
    parser.add_argument('-f', '--first', required=True, type=str,
                        help='First string.')
    parser.add_argument('-s', '--second', required=True, type=str,
                        help='Second string.')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='Verbose output.')
    parser.add_argument('-id', '--indel', required=False, type=int, default=-1,
                        help='Penalty for inserting / deleting.')
    parser.add_argument('-mm', '--mismatch', required=False, type=int, default=-1,
                        help='Penalty for accepting a mismatch.')
    parser.add_argument('-m', '--match', required=False, type=int, default=1,
                        help='Reward for accepting a match.')
    parser.add_argument('-od', '--overlap_detection', action='store_true', required=False,
                        help='Allow for overlap detection')
    args = parser.parse_args()

    main(args.first, args.second, args.verbose, args.indel, args.mismatch, args.match, args.overlap_detection)
