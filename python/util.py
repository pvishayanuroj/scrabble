import time
from functools import wraps

from turns2 import Turn


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Execution time for {func.__module__}.{func.__name__}: {(end_time - start_time):.3f} seconds"
        )
        return result

    return wrapper


def get_all_substrings(word: str) -> set[str]:
    """Returns a set all substrings of the given word.

    Valid substrings are the word itself, all single letters and
    everything in between.
    """
    substrings: set[str] = set()
    for substring_len in range(1, len(word) + 1):
        for start_index in range(len(word) - substring_len + 1):
            substrings.add(word[start_index : (start_index + substring_len)])
    return substrings
