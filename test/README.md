# Deduper Test File Setup

Notes on each chromosome are below, followed by a table indicating the reason for the decision. 
- Chromosome 1 has plus and minus strand reads that all have unique UMIs and should all write out to the new file. 
- Chromosome 2 tests various plus strand read conditions
- Chromosome 3 tests various minus strand read conditions
- Chromosome 4 tests various other conditions



| ID  | Chr | UMI      | Decision | Reason                                                                                            |
| --- | --- | -------- | -------- | ------------------------------------------------------------------------------------------------- |
| 01  | 1   | AACGCCAT | Keep     | New                                                                                               |
| 02  | 1   | AAGGTACG | Keep     | New                                                                                               |
| 03  | 1   | AATTCCGG | Keep     | New                                                                                               |
| 04  | 1   | ACACAGAG | Keep     | New                                                                                               |
| 05  | 2   | CGTTCCAT | Keep     | New                                                                                               |
| 06  | 2   | CGTTCCAT | Toss     | Same as above                                                                                     |
| 07  | 2   | CGTTGGAT | Keep     | New                                                                                               |
| 08  | 2   | CGTTGGAT | Keep     | Same UMI, new position                                                                            |
| 09  | 2   | CGTTGGAT | Toss     | Same pos if soft clip adjusted                                                                    |
| 10  | 2   | CTACGTTC | Keep     | New                                                                                               |
| 11  | 2   | CTACGTTC | Keep     | Softclipping at end to ignore                                                                     |
| 12  | 2   | CTACGTTC | Toss     | Softclipping at both                                                                              |
| 13  | 2   | CGTTCCAT | Toss     | Same UMI and pos as the first entry of ch 2                                                       |
| 14  | 3   | GGATAACG | Keep     | New                                                                                               |
| 15  | 3   | GGATAACG | Toss     | Adjust for M                                                                                      |
| 16  | 3   | GGATAACG | Toss     | Adjust M and trailing S                                                                           |
| 17  | 3   | GGATAACG | Keep     | Skip leading S adjust M  and trailing S                                                           |
| 18  | 3   | GGATAACG | Toss     | Tests for all miscellaneous characters in cigar strings. Should align with the first read of ch 3 |
| 19  | 4   | AACGCCAT | Keep     | Same as first read in file but new chromosome                                                     |
| 20  | 4   | AACGCCAT | Keep     | Same as last but opposite strand                                                                  |
| 21  | 4   | TCGACTTN | Toss     | New but UMI has Ns                                                                                |
