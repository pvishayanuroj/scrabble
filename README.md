# scrabble


## Testcases

New game: 'RSTEOAM'
test3.txt: 'GETHUTO'
test4.txt: 'NRALEFI'

## Performance

Initial timings w/ basic substring check:

**test3**

```
Generated 133363 boards in 33.41 secs
Prune down to 416 boards in 55.70 secs
```

**test4**

```
Generated 1149690 boards in 230.51 secs
Prune down to 970 boards in 420.45 secs
```

Fixed bug where the same branch was being explored, i.e. letters were not being deduped for branch exploration. However, they were incorrectly being deduped when passing the list of remaining letter tiles to the next recursion. e.g. 'GETHUTO' would explore 'GET' twice but miss finding 'GHETTO'.

**test3**

```
Generated 157074 boards in 47.23 secs
Prune down to 324 boards in 65.45 secs
```

**test4**

```
Generated 1149690 boards in 231.68 secs
Prune down to 970 boards in 416.09 secs
```

No change expected, since there are no duplicate letters in the hand tiles.

Implemented further checks to mostly store boards with full words, rather than valid substrings.

**test3**

```
Generated 562 boards in 1.72 secs
Prune down to 182 boards in 0.23 secs
```

**test4**

```
Generated 3221 boards in 13.55 secs
Prune down to 828 boards in 1.18 secs
```

Removed board copying in favor of using the turn structure to track the tile placements. Ended up generating more solutions than the old approach.

**test3**

```
Generated 1870 solutions in 0.70 secs
Pruned down to 323 solutions in 0.96 secs
DEDUP to 203 solutions. TOTAL: 1.66 secs
```

**test4**

```
Generated 9846 solutions in 3.95 secs
Pruned down to 970 solutions in 4.65 secs
DEDUP to 479 solutions. TOTAL: 8.64 secs
```

Made a fix to the original approach since it was missing solutions. On the second letter tile placement, the shape was being incorrectly calculated since the previous and next move were not being considered. Only the previous move, single move was considered.

**test3**

```
Generated 1870 solutions in 0.69 secs
Pruned down to 323 solutions in 0.95 secs
DEDUP to 203 solutions. TOTAL: 1.66 secs

OLD RUN
Generated 1627 boards in 5.75 secs
Prune down to 323 boards in 0.68 secs
DEDUP to 203 solutions. TOTAL: 6.52 secs
0 turns in OLD not in NEW
0 turns in NEW not in OLD
```

**test4**

```
Generated 9846 solutions in 3.87 secs
Pruned down to 970 solutions in 4.61 secs
DEDUP to 479 solutions. TOTAL: 8.53 secs

OLD RUN
Generated 8767 boards in 33.02 secs
Prune down to 970 boards in 3.23 secs
DEDUP to 479 solutions. TOTAL: 36.58 secs
0 turns in OLD not in NEW
0 turns in NEW not in OLD
```

**newgame**

```
Execution time for solver2._initial_expand: 2.342 seconds
Execution time for solver2._filter_valid_turns: 2.168 seconds
Execution time for util.dedup_turns: 57.866 seconds
Generated 6668 initial solutions.
Validation resulted in 6668 solutions.
Deduping resulted in 2464 solutions.
Execution time for solver2.solve: 62.378 seconds

OLD RUN
Generated 6668 boards in 16.54 secs
Prune down to 6668 boards in 1.73 secs
DEDUP to 2464 solutions in 2.03 secs.
TOTAL: 21.92 secs
```

Improved deduping for new approach.

**test3**

```
Execution time for solver2._initial_expand: 0.882 seconds
Execution time for solver2._filter_valid_turns: 0.962 seconds
Execution time for util.dedup_turns: 0.007 seconds
Generated 1870 initial solutions.
Validation resulted in 323 solutions.
Deduping resulted in 203 solutions.
Execution time for solver2.solve: 1.852 seconds

OLD RUN
Generated 1627 boards in 6.08 secs
Prune down to 323 boards in 0.70 secs
DEDUP to 203 solutions in 0.01 secs.
TOTAL: 6.86 secs
```

**test4**

```
Execution time for solver2._initial_expand: 5.111 seconds
Execution time for solver2._filter_valid_turns: 4.380 seconds
Execution time for util.dedup_turns: 0.040 seconds
Generated 9846 initial solutions.
Validation resulted in 970 solutions.
Deduping resulted in 479 solutions.
Execution time for solver2.solve: 9.533 seconds

OLD RUN
Generated 8767 boards in 34.38 secs
Prune down to 970 boards in 3.27 secs
DEDUP to 479 solutions in 0.05 secs.
TOTAL: 37.93 secs
```

**newgame**

```
Execution time for solver2._initial_expand: 2.320 seconds
Execution time for solver2._filter_valid_turns: 2.185 seconds
Execution time for util.dedup_turns: 2.047 seconds
Generated 6668 initial solutions.
Validation resulted in 6668 solutions.
Deduping resulted in 2464 solutions.
Execution time for solver2.solve: 6.553 seconds

OLD RUN
Generated 6668 boards in 16.68 secs
Prune down to 6668 boards in 1.73 secs
DEDUP to 2464 solutions in 2.08 secs.
TOTAL: 22.11 secs
```

## Unit testing

Unit tests need to be run from the python/ directory for some reason. e.g.

```
$ cd python
$ python3 -m unittest test_iterators.py
```
