# BioInformatics - Alignment
Collection of algorithms required for the BioInformatics course at the Computer Lab, Cambridge that relate to sequence alignment.

## Programs
### Unweighted Pair-Group Method with Arithmetic mean (UPGMA)
Creates phylogenetic trees based on a distance matrix, this matrix is best defined using edit distance of the strings.

Use `-v` for a verbose output.
#### Input:
```
python -m Phylogeny.UPGMA -h
```
#### Output:
```
usage: UPGMA.py [-h]

Perform UPGMA on a distance matrix.

options:
  -h, --help  show this help message and exit
```
#### Example:
```
python -m Phylogeny.UPGMA   
{'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, '(b, f)': 0.5, '(a, d)': 4.0, '(g, (b, f))': 6.25, '((a, d), (g, (b, f)))': 8.25, '(c, ((a, d), (g, (b, f))))': 14.5, '(e, (c, ((a, d), (g, (b, f)))))': 17.0}
```