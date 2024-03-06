# scrabble


## Testcases

New game: 'RSTEOAM'
test3.txt: 'GETHUTO'
test4.txt: 'NRALEFI'
test5.txt: 'O*FLTEU'

## Performance

#### Initial timings w/ basic substring check:

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

#### Fixed bug where the same branch was being explored, i.e. letters were not being deduped for branch exploration. However, they were incorrectly being deduped when passing the list of remaining letter tiles to the next recursion. e.g. 'GETHUTO' would explore 'GET' twice but miss finding 'GHETTO'.

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

#### Implemented further checks to mostly store boards with full words, rather than valid substrings.

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

#### Removed board copying in favor of using the turn structure to track the tile placements. Ended up generating more solutions than the old approach.

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

#### Made a fix to the original approach since it was missing solutions. On the second letter tile placement, the shape was being incorrectly calculated since the previous and next move were not being considered. Only the previous move, single move was considered.

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

#### Improved deduping for new approach.

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

**test5**

```
Execution time for solver2._initial_expand: 3.115 seconds
Execution time for solver2._initial_expand: 2.370 seconds
Execution time for solver2._initial_expand: 2.462 seconds
Execution time for solver2._initial_expand: 2.433 seconds
Execution time for solver2._initial_expand: 1.650 seconds
Execution time for solver2._initial_expand: 1.366 seconds
Execution time for solver2._initial_expand: 2.068 seconds
Execution time for solver2._initial_expand: 2.287 seconds
Execution time for solver2._initial_expand: 3.142 seconds
Execution time for solver2._initial_expand: 1.432 seconds
Execution time for solver2._initial_expand: 1.725 seconds
Execution time for solver2._initial_expand: 1.730 seconds
Execution time for solver2._initial_expand: 2.379 seconds
Execution time for solver2._initial_expand: 3.100 seconds
Execution time for solver2._initial_expand: 1.560 seconds
Execution time for solver2._initial_expand: 2.393 seconds
Execution time for solver2._initial_expand: 1.413 seconds
Execution time for solver2._initial_expand: 3.528 seconds
Execution time for solver2._initial_expand: 3.531 seconds
Execution time for solver2._initial_expand: 1.688 seconds
Execution time for solver2._initial_expand: 1.298 seconds
Execution time for solver2._initial_expand: 1.741 seconds
Execution time for solver2._initial_expand: 1.861 seconds
Execution time for solver2._initial_expand: 1.694 seconds
Execution time for solver2._initial_expand: 2.044 seconds
Execution time for solver2._initial_expand: 1.620 seconds
Generated 95246 initial solutions.
Execution time for solver2._filter_valid_turns: 31.678 seconds
Execution time for util.dedup_turns: 18.938 seconds
Generated 95246 initial solutions.
Validation resulted in 44974 solutions.
Deduping resulted in 7288 solutions.
Execution time for solver2.solve: 106.265 seconds
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

#### Reduced the number of initial moves by checking the "cross" word for the first tile. (The number of results are different because I realized I kept using the omit list for testing even though it continually gets updated).

**test3**

```
Execution time for solver2._initial_expand: 0.229 seconds
Generated 387 initial solutions.
Execution time for solver2._filter_valid_turns: 0.186 seconds
Validation resulted in 325 solutions.
Execution time for util.dedup_turns: 0.009 seconds
Deduping resulted in 204 solutions.
Execution time for solver2.solve: 0.424 seconds
```

**test4**

```
Generated 1198 initial solutions.
Execution time for solver2._filter_valid_turns: 0.534 seconds
Validation resulted in 970 solutions.
Execution time for util.dedup_turns: 0.073 seconds
Deduping resulted in 479 solutions.
Execution time for solver2.solve: 1.574 seconds
```

**test5**

```
Execution time for solver2._initial_expand: 1.438 seconds
Execution time for solver2._initial_expand: 1.192 seconds
Execution time for solver2._initial_expand: 1.273 seconds
Execution time for solver2._initial_expand: 1.296 seconds
Execution time for solver2._initial_expand: 0.847 seconds
Execution time for solver2._initial_expand: 0.682 seconds
Execution time for solver2._initial_expand: 1.044 seconds
Execution time for solver2._initial_expand: 1.053 seconds
Execution time for solver2._initial_expand: 1.484 seconds
Execution time for solver2._initial_expand: 0.704 seconds
Execution time for solver2._initial_expand: 0.843 seconds
Execution time for solver2._initial_expand: 0.848 seconds
Execution time for solver2._initial_expand: 1.193 seconds
Execution time for solver2._initial_expand: 1.538 seconds
Execution time for solver2._initial_expand: 0.722 seconds
Execution time for solver2._initial_expand: 1.130 seconds
Execution time for solver2._initial_expand: 0.703 seconds
Execution time for solver2._initial_expand: 1.888 seconds
Execution time for solver2._initial_expand: 1.794 seconds
Execution time for solver2._initial_expand: 0.834 seconds
Execution time for solver2._initial_expand: 0.633 seconds
Execution time for solver2._initial_expand: 0.853 seconds
Execution time for solver2._initial_expand: 0.871 seconds
Execution time for solver2._initial_expand: 0.791 seconds
Execution time for solver2._initial_expand: 0.916 seconds
Execution time for solver2._initial_expand: 0.775 seconds
Generated 45002 initial solutions.
Execution time for solver2._filter_valid_turns: 15.268 seconds
Validation resulted in 45002 solutions.
Execution time for util.dedup_turns: 21.128 seconds
Deduping resulted in 7300 solutions.
Execution time for solver2.solve: 63.750 seconds
```

#### Removed invalid branches which in turn removes the need for validation.

**test3**

```
Execution time for solver2._initial_expand: 0.215 seconds
Generated 325 initial solutions.
Execution time for util.dedup_turns: 0.009 seconds
Deduping resulted in 204 solutions.
Execution time for solver2.solve: 0.224 seconds
```

**test4**

```
Execution time for solver2._initial_expand: 0.898 seconds
Generated 970 initial solutions.
Execution time for util.dedup_turns: 0.045 seconds
Deduping resulted in 479 solutions.
Execution time for solver2.solve: 0.944 seconds
```

**test5**

```
Execution time for solver2._initial_expand: 1.510 seconds
Execution time for solver2._initial_expand: 1.250 seconds
Execution time for solver2._initial_expand: 1.325 seconds
Execution time for solver2._initial_expand: 1.350 seconds
Execution time for solver2._initial_expand: 0.877 seconds
Execution time for solver2._initial_expand: 0.713 seconds
Execution time for solver2._initial_expand: 1.091 seconds
Execution time for solver2._initial_expand: 1.133 seconds
Execution time for solver2._initial_expand: 1.597 seconds
Execution time for solver2._initial_expand: 0.758 seconds
Execution time for solver2._initial_expand: 0.915 seconds
Execution time for solver2._initial_expand: 0.911 seconds
Execution time for solver2._initial_expand: 1.298 seconds
Execution time for solver2._initial_expand: 1.808 seconds
Execution time for solver2._initial_expand: 0.789 seconds
Execution time for solver2._initial_expand: 1.229 seconds
Execution time for solver2._initial_expand: 0.759 seconds
Execution time for solver2._initial_expand: 1.908 seconds
Execution time for solver2._initial_expand: 1.938 seconds
Execution time for solver2._initial_expand: 0.901 seconds
Execution time for solver2._initial_expand: 0.683 seconds
Execution time for solver2._initial_expand: 0.922 seconds
Execution time for solver2._initial_expand: 0.938 seconds
Execution time for solver2._initial_expand: 0.843 seconds
Execution time for solver2._initial_expand: 0.996 seconds
Execution time for solver2._initial_expand: 0.839 seconds
Generated 45002 initial solutions.
Execution time for util.dedup_turns: 20.919 seconds
Deduping resulted in 7300 solutions.
Execution time for solver2.solve: 50.211 seconds
```

## Unit testing

Unit tests need to be run from the python/ directory for some reason. e.g.

```
$ cd python
$ python3 -m unittest test_iterators.py
```
