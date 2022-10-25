import argparse

# Dynamic programming implementation of Smith-Waterman Alignment
# Interactive demo: https://bioboot.github.io/bimm143_W20/class-material/nw/


def swa(string_one: str, string_two: str, verbose: bool = False,
        match: int = 1, mismatch: int = -1, indel: int = -1):
    """
    Calculate the local alignments of two strings
    :param string_one: The first string
    :param string_two: The second string
    :param verbose: Should the function be verbose
    :param match: Reward for finding a match
    :param mismatch: Penalty for accepting a mismatch
    :param indel: Penalty for accepting an insert / delete
    :return: The local alignment of {StringOne} and {StringTwo}
    """

    m = len(string_one)
    n = len(string_two)

    L = [[0 for x in range(n + 1)] for x in range(m + 1)]
    backtrace = [[' ' for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m+1):
        backtrace[i][0] = 'E'
    for j in range(n+1):
        backtrace[0][j] = 'E'


    # Following steps build L[m+1][n+1] in bottom up fashion. Note
    # that L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1]
    if verbose:
        print(f'Finding the Longest Common Subsequence of {string_one} and {string_two}\n')
        print(f'1. Producing the graph:')

    max_score = 0
    max_locations = []

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diagonal = L[i-1][j-1] + (match if string_one[i-1] == string_two[j-1] else mismatch)
            up = L[i-1][j] + indel
            left = L[i][j-1] + indel

            new_max = max(diagonal, up, left)
            if new_max > max_score:
                max_score = new_max
                max_locations = [(i, j)]
            elif new_max == max_score:
                max_locations.append((i, j))

            if diagonal <= 0 and up <= 0 and left <= 0:
                L[i][j] = 0
                backtrace[i][j] = 'E'
            elif diagonal >= left and diagonal >= up:
                L[i][j] = diagonal
                backtrace[i][j] = 'D'
            elif up >= diagonal and up >= left:
                L[i][j] = up
                backtrace[i][j] = 'U'
            else:
                L[i][j] = left
                backtrace[i][j] = 'L'

    index = L[m][n]

    if verbose:
        print(f'\t       {" ".join([(" " * (len(str(index)))) + i for i in list(string_two)])}')
        print(f'\t{"-" * (n * (len(str(index)) + 2) + 6)}')
        for col, letter in zip(L, list(' ' + string_one)):
            print(f'\t{letter} | {" ".join([(" " * (len(str(index)) + 1 - len(str(i)))) + str(i) for i in col])}')
        print()

        print(f'\t       {" ".join([(" " * (len(str(index)))) + i for i in list(string_two)])}')
        print(f'\t{"-" * (n * (len(str(index)) + 2) + 6)}')
        for col, letter in zip(backtrace, list(' ' + string_one)):
            print(f'\t{letter} | {" ".join([(" " * (len(str(index)) + 1 - len(str(i)))) + str(i) for i in col])}')
        print()


    if verbose:
        print('2. Navigating the graph (backtracking):')

    to_return = []
    for i, j in max_locations:
        to_return_one = ""
        to_return_two = ""

        if verbose:
            print(f'\tStarting from ({i}, {j})')

        while i > 1 or j > 1:
            current = backtrace[i-1][j-1]
            done = False
            if current == 'D':
                i -= 1
                j -= 1
                to_return_one = string_one[i-1] + to_return_one
                to_return_two = string_two[j-1] + to_return_two
            elif current == 'L':
                j -= 1
                to_return_one = '-' + to_return_one
                to_return_two = string_two[j-1] + to_return_two
            elif current == 'U':
                i -= 1
                to_return_one = string_one[i-1] + to_return_one
                to_return_two = '-' + to_return_two
            else:
                to_return_one = string_one[i-1] + to_return_one
                to_return_two = string_two[j-1] + to_return_two
                to_return.append((to_return_one, to_return_two))
                done = True
            if verbose:
                print(f'\t\tMoving {current}, Updating strings:\n\t\t\t{to_return_one}\n\t\t\t{to_return_two}')
            if done:
                break

    return to_return


def main(first_string: str, second_string: str, verbose: bool = False,
         indel: int = -1, mismatch: int = -1, match: int = 1):
    local_alignment = swa(first_string, second_string, verbose, match, mismatch, indel)
    print(f'Local Alignment of "{first_string}" and "{second_string}":')
    for string_one, string_two in local_alignment:
        print(f'{string_one} & \n{string_two}')




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the optimal local alignment of two strings.')
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
    args = parser.parse_args()

    main(args.first, args.second, args.verbose, args.indel, args.mismatch, args.match)


