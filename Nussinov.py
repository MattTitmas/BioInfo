import argparse

# Implementaion of the Nussinov Folding Alogrithm
# Interactive demo: https://rna.informatik.uni-freiburg.de/Teaching/index.jsp?toolName=Nussinov

def couple(a, b):
    """
    Return True if RNA nucleotides are Watson-Crick base pairs
    """
    pairs = {"A": "U", "U": "A", "G": "C", "C": "G"}  # ...or a list of tuples...
    # check if pair is a couple
    if (a, b) in pairs.items():
        return True

    return False

def traceback(L, rna, fold, i, j, verbose=True, tabs: int = 0):
    if i < j:
        if L[i][j] == L[i + 1][j]: # 1st rule
            traceback(L, rna, fold, i + 1, j)
        elif L[i][j] == L[i][j - 1]: # 2nd rule
            traceback(L, rna, fold, i, j - 1)
        elif L[i][j] == L[i + 1][j - 1] + couple(rna[i], rna[j]): # 3rd rule
            fold.append((i, j))
            traceback(L, rna, fold, i + 1, j - 1)
        else:
            for k in range(i + 1, j - 1):
                if L[i][j] == L[i, k] + L[k + 1][j]: # 4th rule
                    traceback(L, rna, fold, i, k)
                    traceback(L, rna, fold, k + 1, j)
                    break
                    # break to only find 1 solution

    return fold


def nussinov(RNA, minimum_loop_length: int = 0, verbose: bool = False,
             complementary: int = 1, uncomplementary: int = 0):
    L = [[0 for x in range(len(RNA))] for y in range(len(RNA))]

    if verbose:
        print('1. Generating the matrix:')
    for diag in range(1, len(RNA)):
        if verbose:
            print(f'\tCreating diagonal {diag}:\n\t  ', end='')
        for i in range(0, len(RNA) - diag):
            j = i + diag
            maximum = 0
            if j - i > minimum_loop_length:
                down = L[i+1][j]
                left = L[i][j-1]
                diagonal_complementary = L[i+1][j-1] + (complementary if couple(RNA[i], RNA[j]) else uncomplementary)

                k_max = max([L[i][k] + L[k+1][j] for k in range(i+1, j)], default=-float('inf'))
                maximum = max(down, left, diagonal_complementary, k_max)

            if verbose:
                print(f'{maximum} ', end='')
            L[i][j] = maximum
        if verbose:
            print()

    if verbose:
        print('\n\tThe final matrix:')
        for count, l in enumerate(L):
            print('\t     ',end='')
            for count_inner, i in enumerate(l):
                if count_inner < count:
                    print('  ', end='')
                else:
                    print(f'{i} ', end='')
            print('')

    if verbose:
        print('2. Performing traceback on the matrix:')
    fold = traceback(L, RNA, [], 0, len(RNA)-1, verbose=verbose)

    dot = ["." for i in range(len(RNA))]
    for s in fold:
        dot[min(s)] = "("
        dot[max(s)] = ")"
    return "".join(dot)




def main(RNA: str, minimum_loop_length: int, verbose: bool = False):
    print(nussinov(RNA, minimum_loop_length=minimum_loop_length, verbose=verbose))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a folding for a RNA sequence')
    parser.add_argument('-R', '--RNA', required=True, type=str,
                        help='RNA Sequence.')
    parser.add_argument('-mll', '--minimum_loop_length', type=int, required=False, default=1,
                        help='The minimum length allowed for a loop.')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='Verbose output.')
    args = parser.parse_args()

    main(args.RNA, args.minimum_loop_length, args.verbose)
