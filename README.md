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
