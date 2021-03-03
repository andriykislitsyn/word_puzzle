from pathlib import Path


def read_test_words():
    with open(TEST_WORDS_CONTAINER) as dictionary:
        return dictionary.read().splitlines()


PROD_WORDS_CONTAINER = Path(__file__).parents[1].joinpath('data/words.txt')
TEST_WORDS_CONTAINER = Path(__file__).parents[1].joinpath('data/test_words.txt')
TEST_WORDS_NUMBER = 100
TEST_WORDS = read_test_words()
TEST_NODES = 21
TEST_GRID = [
    ['A', 'O', 'G', 'B', 'Q', 'P', 'R', 'B', 'H', 'C', 'R', 'E', 'D', 'G', 'A'],
    ['X', 'D', 'G', 'H', 'V', 'J', 'I', 'F', 'D', 'J', 'J', 'F', 'L', 'F', 'O'],
    ['P', 'A', 'T', 'P', 'M', 'H', 'K', 'U', 'Z', 'O', 'V', 'Y', 'Y', 'C', 'I'],
    ['Y', 'W', 'S', 'U', 'H', 'X', 'M', 'Z', 'S', 'U', 'M', 'S', 'Z', 'P', 'A'],
    ['V', 'B', 'O', 'J', 'R', 'Y', 'L', 'E', 'V', 'L', 'R', 'B', 'N', 'T', 'I'],
    ['D', 'W', 'U', 'B', 'Y', 'N', 'S', 'M', 'Q', 'O', 'Q', 'J', 'R', 'V', 'X'],
    ['A', 'C', 'E', 'S', 'C', 'F', 'P', 'I', 'O', 'U', 'P', 'Y', 'B', 'C', 'K'],
    ['Z', 'O', 'B', 'P', 'H', 'G', 'O', 'I', 'O', 'M', 'I', 'B', 'R', 'U', 'F'],
    ['R', 'X', 'E', 'Y', 'D', 'M', 'W', 'R', 'K', 'L', 'R', 'W', 'Z', 'J', 'M'],
    ['Q', 'E', 'B', 'I', 'D', 'R', 'A', 'O', 'T', 'E', 'O', 'O', 'E', 'L', 'V'],
    ['O', 'L', 'M', 'O', 'A', 'H', 'S', 'N', 'V', 'U', 'S', 'G', 'H', 'D', 'A'],
    ['O', 'Q', 'E', 'O', 'I', 'W', 'V', 'E', 'Y', 'A', 'N', 'A', 'I', 'Q', 'X'],
    ['X', 'X', 'M', 'T', 'T', 'Q', 'U', 'R', 'Z', 'E', 'T', 'A', 'K', 'S', 'W'],
    ['J', 'F', 'Y', 'P', 'I', 'E', 'H', 'H', 'H', 'P', 'Y', 'N', 'T', 'I', 'T'],
    ['T', 'Q', 'I', 'R', 'U', 'G', 'S', 'O', 'V', 'P', 'K', 'E', 'F', 'E', 'Y'], ]

IMPLANTED_WORDS = (('BUSHMAN', (1, 4), (7, 10)), ('EMOTES', (1, 9), (6, 14)), ('FORTUNATE', (5, 6), (13, 14)),
                   ('PHYSIOLOGIST', (3, 2), (14, 13)), ('TURNPIKES', (2, 2), (10, 10)))

WORST_PERFORMANCE_THRESHOLD = 500  # Solution must be found within 500ms.
