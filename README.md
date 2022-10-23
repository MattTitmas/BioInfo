# BioInfo
Collection of algorithms required for the BioInformatics course at the Computer Lab, Cambridge

## Programs
### Longest Common Subsequence (LCS)
Calculates the longest common subsequence of two strings, this is the longest non-continuous string that can be found in the two input strings.

Use `-v` for a verbose output.
#### Input:
```
python -m LCS -h
```
#### Output:
```
usage: LCS.py [-h] -f FIRST -s SECOND [-v]

Find the longest common subsequence of two strings.

options:
  -h, --help            show this help message and exit
  -f FIRST, --first FIRST
                        First string.
  -s SECOND, --second SECOND
                        Second string.
  -v, --verbose         Verbose output.
```
#### Example:
```
python -m LCS -f XMJYAUZ -s MZJAWXU
Longest Common Subsequence of "XMJYAUZ" and "MZJAWXU": MJAU
```

### Needleman-Wunsch Algorithm (NWA)
Calculates the global alignment of two strings, this is the optimal way to manipulate the two strings such that they are equal with the minimal edit-distance.

Use `-v` for a verbose output.
#### Input:
```
python -m NWA -h
```
#### Output:
```
usage: NWA.py [-h] -f FIRST -s SECOND [-v] [-od]

Find the longest common subsequence of two strings.

options:
  -h, --help            show this help message and exit
  -f FIRST, --first FIRST
                        First string.
  -s SECOND, --second SECOND
                        Second string.
  -v, --verbose         Verbose output.
  -od, --overlap_detection
                        Allow for overlap detection
```
#### Example:
```
python -m LCS -f XMJYAUZ -s MZJAWXU
Global Alignment of "XMJYAUZ" and "MZJAWXU": 
XM-JYA--UZ &
-MZJ-AWXU-
```

### Smith-Waterman Algorithm (NWA)
Calculates the local alignments of two strings

Use `-v` for a verbose output.
#### Input:
```
python -m SWA -h
```
#### Output:
```
usage: SWA.py [-h] -f FIRST -s SECOND [-v]

Find the longest common subsequence of two strings.

options:
  -h, --help            show this help message and exit
  -f FIRST, --first FIRST
                        First string.
  -s SECOND, --second SECOND
                        Second string.
  -v, --verbose         Verbose output.
```
#### Example:
```
python -m SWA -f ABCD -s BCAB 
Local Alignment of "ABCD" and "BCAB":
AA &
AA
BB &
BB
```