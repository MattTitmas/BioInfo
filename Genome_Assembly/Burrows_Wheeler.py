import argparse


def burrows_wheeler_transform(string: str, verbose: bool = False) -> str:
    sentinel_String = (string + '$')
    # To emulate cycling back to the beginning
    double_sentinel_string = sentinel_String * 2

    # Generate the matrix of left-rotated strings
    burrows_wheeler_matrix = [
        list(double_sentinel_string[i:i + len(string) + 1]) for i in range(len(string) + 1)
    ]
    if verbose:
        print(f'The generated unsorted Burrows-Wheeler matrix is:')
        for i in burrows_wheeler_matrix:
            print(f'\t{" ".join(i)}')
        print()
        print(f'The generated sorted Burrows-Wheeler matrix is:')
        for i in sorted(burrows_wheeler_matrix):
            print(f'\t{" ".join(i)}')
        print()



    # Take the last column
    return ''.join(map(lambda x: x[-1], burrows_wheeler_matrix))


def burrows_wheeler_transform_suffix_array(string: str, verbose: bool = False) -> str:
    sentinel_string = (string + '$')
    # Generate a stored suffix array but also store the original position before sorting
    suffix_array = [(sentinel_string[i:], i) for i in range(len(sentinel_string))]
    if verbose:
        print(f'The generated unsorted Burrows-Wheeler suffix array is:')
        for i in suffix_array:
            print(f'\t{i}')
        print()

        print(f'The generated sorted Burrows-Wheeler suffix array is:')
        for i in sorted(suffix_array):
            print(f'\t{i}')
        print()

    suffix_array = sorted(suffix_array)

    # Generate the BWT of the string from the suffix array
    return ''.join([sentinel_string[suffix_array[i][1] - 1] if suffix_array[i][1] > 0 else '$'
                    for i in range(len(sentinel_string))])


def inverse_burrows_wheeler_inefficient(string: str) -> str:
    inverse_matrix = [['' for i in range(len(string))] for i in range(len(string))]
    for count, i in enumerate(sorted(string)):
        inverse_matrix[count][0] = i
        inverse_matrix[count][-1] = string[count]

    # Already have first and last column, therefore just need n - 2 more
    for i in range(1, len(string) - 1):
        for count, j in enumerate(sorted(map(lambda x: x[-1] + ''.join(x[:-1]), inverse_matrix))):
            inverse_matrix[count][i] = j[-1]

    # Remove the $ That was added in during BWT
    return ''.join(inverse_matrix[0])[1:]


def inverse_burrows_wheeler(string: str, verbose: bool = False) -> str:
    last_row = [(i, string[:count].count(i)) for count, i in enumerate(string)]
    first_row = sorted(last_row)
    current, value = '', 0
    index = last_row.index(('$', 0))
    reconstructed_string = ''
    print('Inversing the transformed string')
    while current != '$':
        if verbose:
            print(f'\tCurrent index is: ({current if current != "" else "$"}, {value})')
        current, value = first_row[index]
        reconstructed_string += current
        index = last_row.index((current, value))

    # Remove the $ That was added in during BWT
    return reconstructed_string[:-1]


def RLE(string: str) -> str:
    sentence = []
    current_count = 0
    for c1, c2 in zip(string, string[1:] + '$'):
        current_count += 1
        if c1 != c2:
            if current_count != 1 and current_count != 2:
                sentence.append(str(current_count))
            sentence.append(c1)
            current_count = 0
    return ''.join(sentence)



def main(string: str, verbose: bool = False):
    encoded_string = burrows_wheeler_transform_suffix_array(string, verbose)
    compressed = RLE(encoded_string)
    decoded_string = inverse_burrows_wheeler(encoded_string, verbose)

    print(f'The BWT of {string} is:\n\t{encoded_string}.\nThis, when encoded with RLE is:\n\t{compressed}')
    print(f'It saves {round(100*(len(RLE(string)) - len(compressed))/len(RLE(string)),2)}% space.')
    print(f'The deocded string is:\n\t{decoded_string}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform the Burrows-Wheeler transform and inverse on a given string.")
    parser.add_argument('-s', '--string', type=str, required=True,
                        help='Word to perform the transform on.')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='Verbose output.')
    args = parser.parse_args()

    main(args.string, args.verbose)
