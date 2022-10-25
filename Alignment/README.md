# BioInformatics - Alignment
Collection of algorithms required for the BioInformatics course at the Computer Lab, Cambridge that relate to sequence alignment.

## Programs
### Longest Common Subsequence (LCS)
Calculates the longest common subsequence of two strings, this is the longest non-continuous string that can be found in the two input strings.

Use `-v` for a verbose output.
#### Input:
```
python -m ALignment.LCS -h
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
python -m Alignment.LCS -f XMJYAUZ -s MZJAWXU
Longest Common Subsequence of "XMJYAUZ" and "MZJAWXU": MJAU
```

### Needleman-Wunsch Algorithm (NWA)
Calculates the global alignment of two strings, this is the optimal way to manipulate the two strings such that they are equal with the minimal edit-distance.

Use `-v` for a verbose output.
#### Input:
```
python -m Alignment.NWA -h
```
#### Output:
```
usage: NWA.py [-h] -f FIRST -s SECOND [-v] [-id INDEL] [-mm MISMATCH] [-m MATCH] [-od]

Find the optimal global alignment of two strings.

options:
  -h, --help            show this help message and exit
  -f FIRST, --first FIRST
                        First string.
  -s SECOND, --second SECOND
                        Second string.
  -v, --verbose         Verbose output.
  -id INDEL, --indel INDEL
                        Penalty for inserting / deleting.
  -mm MISMATCH, --mismatch MISMATCH
                        Penalty for accepting a mismatch.
  -m MATCH, --match MATCH
                        Reward for accepting a match.
  -od, --overlap_detection
                        Allow for overlap detection.
```
#### Example:
```
python -m Alignment.NWA -f XMJYAUZ -s MZJAWXU
Global Alignment of "XMJYAUZ" and "MZJAWXU": 
XM-JYA--UZ &
-MZJ-AWXU-
```

### Smith-Waterman Algorithm (NWA)
Calculates the local alignments of two strings

Use `-v` for a verbose output.
#### Input:
```
python -m Alignment.SWA -h
```
#### Output:
```
usage: SWA.py [-h] -f FIRST -s SECOND [-v] [-id INDEL] [-mm MISMATCH] [-m MATCH]

Find the optimal local alignment of two strings.

options:
  -h, --help            show this help message and exit
  -f FIRST, --first FIRST
                        First string.
  -s SECOND, --second SECOND
                        Second string.
  -v, --verbose         Verbose output.
  -id INDEL, --indel INDEL
                        Penalty for inserting / deleting.
  -mm MISMATCH, --mismatch MISMATCH
                        Penalty for accepting a mismatch.
  -m MATCH, --match MATCH
                        Reward for accepting a match.
```
#### Example:
```
python -m Alignment.SWA -f ABCD -s BCAB 
Local Alignment of "ABCD" and "BCAB":
AA &
AA
BB &
BB
```

### Hirschberg's Algorithm (Hirschberg)
Calculates the global alignment of two strings, using linear space (With respect to the length of the strings)

Use `-v` for a verbose output.
#### Input:
```
python -m Alignment.Hirschberg -h
```
#### Output:
```
usage: Hirschberg.py [-h] -f FIRST -s SECOND [-v] [-id INDEL] [-mm MISMATCH] [-m MATCH]

Find the optimal global alignment of two strings.

options:
  -h, --help            show this help message and exit
  -f FIRST, --first FIRST
                        First string.
  -s SECOND, --second SECOND
                        Second string.
  -v, --verbose         Verbose output.
  -id INDEL, --indel INDEL
                        Penalty for inserting / deleting.
  -mm MISMATCH, --mismatch MISMATCH
                        Penalty for accepting a mismatch.
  -m MATCH, --match MATCH
                        Reward for accepting a match.
```
#### Example:
```
python -m Alignment.Hirschberg -f XMJYAUZ -s MZJAWXU
Global Alignment of "XMJYAUZ" and "MZJAWXU":
XM-JYA--UZ &
-MZJ-AWXU-
```

### Nussinov's Folding Algorithm
Calculates the optimal folding for a given sequence of RNA bases.

Use `-v` for a verbose output.
#### Input:
```
python -m Alignment.Hirschberg -h
```
#### Output:
```
usage: Nussinov.py [-h] -R RNA [-mll MINIMUM_LOOP_LENGTH] [-v]

Generate a folding for a RNA sequence

options:
  -h, --help            show this help message and exit
  -R RNA, --RNA RNA     RNA Sequence.
  -mll MINIMUM_LOOP_LENGTH, --minimum_loop_length MINIMUM_LOOP_LENGTH
                        The minimum length allowed for a loop.
  -v, --verbose         Verbose output.
```
#### Example:
```
python -m Alignment.Nussinov -R GGGAAAUCC
Optimal fold for GGGAAAUCC with a minimum loop length of 1:
        .((.(.)))

```