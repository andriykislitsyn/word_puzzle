import random
from timeit import default_timer as timer

import pytest

from grid_builder import GridBuilder
from tests.data import TEST_GRID, TEST_NODES, TEST_WORDS, TEST_WORDS_CONTAINER, TEST_WORDS_NUMBER, IMPLANTED_WORDS, PROD_WORDS_CONTAINER, \
    WORST_PERFORMANCE_THRESHOLD
from utils import BookWorm
from word_search import WordSearchSolver, WordTree, WordNode


@pytest.fixture(scope='module')
def bookworm():
    yield BookWorm(data_file=TEST_WORDS_CONTAINER, longest_word=len(TEST_GRID))


class TestBookWorm:
    def test_words_list_number(self, bookworm):
        assert len(bookworm.words) == TEST_WORDS_NUMBER

    def test_words_list_type(self, bookworm):
        assert isinstance(bookworm.words, list)

    def test_word_type(self, bookworm):
        assert isinstance(random.choice(bookworm.words), str)

    def test_word_isupper(self, bookworm):
        assert random.choice(bookworm.words).isupper()

    def test_word_length(self, bookworm):
        assert len(random.choice(bookworm.words)) <= len(TEST_GRID)


class TestGridBuilder:
    unit: GridBuilder = GridBuilder()

    def test_grid_after_initialization(self):
        assert isinstance(self.unit.grid, list)
        assert isinstance(self.unit.grid[random.randint(1, self.unit.side - 1)], list)

    def test_grid_item(self):
        item = self.unit.grid[random.randint(1, self.unit.side - 1)][random.randint(1, self.unit.side - 1)]
        assert isinstance(item, str)
        assert item.isupper()

    def test_grid_creation_with_hidden_words_specified(self):
        words_to_hide = ['sambaing', 'redistrict', 'argosy', 'caesuras']
        grid = GridBuilder(words_to_hide=words_to_hide)
        assert isinstance(self.unit.grid, list)
        assert isinstance(self.unit.grid[random.randint(1, self.unit.side - 1)], list)
        assert sorted((w[0] for w in grid.implanted_words)) == sorted(w.upper() for w in words_to_hide)

    def test_attempt_inserting_word_that_is_too_long(self):
        words_to_hide = ['sambaing', 'redistrict', 'argosy', 'caesuras']
        with pytest.raises(ValueError):
            assert GridBuilder(words_to_hide=words_to_hide, side=max(len(w) for w in words_to_hide) - 1)


class TestWordTree:
    unit: WordTree = WordTree()
    nodes: int = 0

    def test_empty_word_tree(self):
        assert isinstance(self.unit.root, WordNode)
        assert not self.unit.root.children

    @pytest.mark.parametrize('word', TEST_WORDS)
    def test_add_word_to_tree(self, word):
        self.unit.add_word(word)
        assert len(self.unit.root.children) > self.nodes
        self.nodes += 1

    def test_first_node_of_the_tree(self):
        assert self.unit.root.children[0].char == 'a'

    def test_last_node_of_the_tree(self):
        assert self.unit.root.children[-1].char == 'z'

    def test_nodes_number(self):
        assert 0 < len(self.unit.root.children) <= 26


class TestWordSearchSolver:
    unit: WordSearchSolver = WordSearchSolver([w.upper() for w in TEST_WORDS])

    def test_word_tree_creation(self):
        assert isinstance(self.unit.tree, WordTree)
        assert isinstance(self.unit.tree.root, WordNode)
        assert len(self.unit.tree.root.children) == TEST_NODES

    def test_initial_grid_parameters(self):
        assert self.unit.side == 0
        assert self.unit.grid == []

    def test_grid_slices(self):
        self.unit.grid = TEST_GRID
        self.unit.side = len(TEST_GRID)
        for grid_slice in self.unit.grid_slices:
            assert isinstance(grid_slice, list)
            assert 1 <= len(grid_slice) <= self.unit.side
            for char in grid_slice:
                assert char.isupper()

    def test_grid_solution(self):
        result = self.unit.solve(TEST_GRID)
        assert set(IMPLANTED_WORDS).issubset(set(result))


class TestWordPuzzle:
    grid = None
    bookworm = None
    solver = None
    solution = None

    def test_components_creation(self):
        book_worm = BookWorm(PROD_WORDS_CONTAINER)
        TestWordPuzzle.bookworm = book_worm
        longest_known_word = len(sorted(book_worm.words, key=len)[-1])
        TestWordPuzzle.grid = GridBuilder(
            words_to_hide=random.choices(book_worm.words, k=random.randint(3, 6)),
            side=random.randint(longest_known_word + 1, 30))
        TestWordPuzzle.solver = WordSearchSolver(book_worm.words)

    def test_solve_word_puzzle(self):
        solution = self.solver.solve(self.grid.grid)
        assert solution
        assert isinstance(solution, list)
        TestWordPuzzle.solution = solution

    def test_solved_item_type(self):
        item = random.choice(self.solution)
        assert isinstance(item, tuple)
        assert isinstance(item[0], str)
        assert item[0].isalpha()
        assert isinstance(item[1:], (tuple, tuple))
        start, end = item[1], item[2]
        assert isinstance(start[0], int), isinstance(start[1], int)
        assert isinstance(end[0], int), isinstance(end[1], int)

    def test_all_hidden_words_found(self):
        assert set(self.grid.implanted_words).issubset(set(self.solution))

    def test_all_known_words_found(self):
        assert set((w[0] for w in self.solution)).issubset(set(self.bookworm.words))

    def test_solution_time(self):
        bookworm = BookWorm(data_file=PROD_WORDS_CONTAINER, longest_word=12)
        for _ in range(100):
            grid = GridBuilder(words_to_hide=random.choices(bookworm.words, k=random.randint(3, 6)))
            start = timer()
            self.solver.solve(grid.grid)
            end = timer()
            assert 1000 * (end - start) < WORST_PERFORMANCE_THRESHOLD, f'Solution took: {round(1000 * (end - start), 4)} ms'
