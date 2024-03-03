# scrabble


## Testcases

test3.txt: 'GETHUTO'
test4.txt: 'NRALEFI'

## Development

Initial timings w/ basic substring check:

test3

Generated 133363 boards in 33.41 secs
Prune down to 416 boards in 55.70 secs

test4

Generated 1149690 boards in 230.51 secs
Prune down to 970 boards in 420.45 secs

Fixed bug where the same branch was being explored, i.e. letters were not being deduped for branch exploration. However, they were incorrectly being deduped when passing the list of remaining letter tiles to the next recursion. e.g. 'GETHUTO' would explore 'GET' twice but miss finding 'GHETTO'.

test3

Generated 157074 boards in 47.23 secs
Prune down to 324 boards in 65.45 secs

test4

Generated 1149690 boards in 231.68 secs
Prune down to 970 boards in 416.09 secs

No change expected, since there are no duplicate letters in the hand tiles.

Implemented further checks to mostly store boards with full words, rather than valid substrings.

test3

Generated 562 boards in 1.72 secs
Prune down to 182 boards in 0.23 secs

test4

Generated 3221 boards in 13.55 secs
Prune down to 828 boards in 1.18 secs

Removed board copying in favor of using the turn structure to track the tile placements. Ended up generating more solutions than the old approach.

test3

Generated 1870 solutions in 0.70 secs
Pruned down to 323 solutions in 0.96 secs
DEDUP to 203 solutions. TOTAL: 1.66 secs

test4

Generated 9846 solutions in 3.95 secs
Pruned down to 970 solutions in 4.65 secs
DEDUP to 479 solutions. TOTAL: 8.64 secs

Made a fix to the original approach since it was missing solutions. On the second letter tile placement, the shape was being incorrectly calculated since the previous and next move were not being considered. Only the previous move, single move was considered.

test3

Generated 1870 solutions in 0.69 secs
Pruned down to 323 solutions in 0.95 secs
DEDUP to 203 solutions. TOTAL: 1.66 secs
OLD RUN
Generated 1627 boards in 5.75 secs
Prune down to 323 boards in 0.68 secs
DEDUP to 203 solutions. TOTAL: 6.52 secs
0 turns in OLD not in NEW
0 turns in NEW not in OLD

test4

Generated 9846 solutions in 3.87 secs
Pruned down to 970 solutions in 4.61 secs
DEDUP to 479 solutions. TOTAL: 8.53 secs
OLD RUN
Generated 8767 boards in 33.02 secs
Prune down to 970 boards in 3.23 secs
DEDUP to 479 solutions. TOTAL: 36.58 secs
0 turns in OLD not in NEW
0 turns in NEW not in OLD

## Unit testing

Unit tests need to be run from the python/ directory for some reason. e.g.

```
$ cd python
$ python3 -m unittest test_iterators.py
```
