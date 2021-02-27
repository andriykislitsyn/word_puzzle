from itertools import chain
from typing import List, Tuple


class WordNode:
    """
        Node object for the WordTree data structure.

        Attributes:
          char - value of the node.
          children - list of child node objects.
          my_word - if this node completes a word, my_word is assigned to that word, else it equals to "".
    """

    __slots__ = ('char', 'children', 'my_word')

    def __init__(self, char: str = ''):
        self.char: str = char
        self.children: List[WordNode] = list()
        self.my_word: str = ''

    def add_child(self, char: str):
        """Create a new child WordNode object, assigning it with the given character."""
        child = WordNode(char)
        self.children.append(child)
        return child

    def get_child(self, char: str):
        """Return the child WordNode with the given character, if it exists."""
        for child in self.children:
            if child.char == char:
                return child


class WordTree:
    """
        Tree data structure object, used as an efficient method for
        checking word spelling. All words added form a path from the
        root node, with each node representing a letter of that word.

        Attributes:
          root - root of the tree.
    """

    __slots__ = ('root',)

    def __init__(self):
        self.root = WordNode()

    def add_word(self, word):
        """Adds a word into the tree data structure."""
        parent = self.root
        for char in word:
            child = parent.get_child(char)
            if not child:
                child = parent.add_child(char)
            parent = child
        parent.my_word = word


class WordSearchSolver:
    """
        Class solving a Word Search puzzle.

        Attributes:
          tree - tree data structure object holding known words.
          side - length of the grid side.
          grid - the grid (2d matrix of letters).
    """

    def __init__(self, known_words: List[str], tree=WordTree()):
        self.tree = tree
        self.known_words = known_words
        self.grid: List[List[str]] = list()
        self.side: int = 0
        self.slice_funcs = [self._slices_north, self._slices_south, self._slices_west, self._slices_east,
                            self._slices_north_west, self._slices_north_east,
                            self._slices_south_west, self._slices_south_east]
        for word in self.known_words:
            self.tree.add_word(word)

    def solve(self, grid: List[List[str]]) -> List[Tuple[str, Tuple[int, int], Tuple[int, int]]]:
        """
            Find the positions of all hidden words.

            params:
              grid (list) - 2d matrix of letters, representing the word search grid to be solved

            return:
              found_words (list) - a list of tuples containing:
                word (str) : hidden word
                start_pos (int, int) : x, y position of the start of the word
                end_pos (int, int) : x, y position of the end of the word
        """
        self.side = len(grid)
        self.grid = tuple(tuple(((col, row), grid[row][col]) for col in range(self.side)) for row in range(self.side))

        found_words = list()
        for grid_slice in self.grid_slices:
            for solution in self._find_words(grid_slice):
                found_words.append(solution)
        return found_words

    @property
    def grid_slices(self):
        """
            Generator function used to extract grid slices.

            yield:
              grid_slice - a grid slice of the word search grid, in the given `direction`
        """
        for grid_slice in chain(*(func() for func in self.slice_funcs)):
            yield grid_slice

    def _find_words(self, grid_slice):
        """
            Generator function for finding words in a word search grid slice.

            params:
              grid_slice - a slice of the word search grid.

            yield:
              word - a word found in the grid slice.
        """
        for i, (start_position, char) in enumerate(grid_slice):
            if not self.tree.root.get_child(char):
                continue
            node = self.tree.root.get_child(char)
            for end_position, next_char in grid_slice[i + 1:]:
                node = node.get_child(next_char)
                if not node:
                    break
                if node.my_word:
                    yield node.my_word, start_position, end_position

    def _slices_north(self):
        """Yield grid slices in a north direction."""
        for col in range(self.side):
            grid_slice = list()
            for row in range(self.side - 1, -1, -1):
                grid_slice.append(self.grid[row][col])
            yield grid_slice

    def _slices_south(self):
        """Yield grid slices in a south direction."""
        for col in range(self.side):
            grid_slice = list()
            for row in range(self.side):
                grid_slice.append(self.grid[row][col])
            yield grid_slice

    def _slices_west(self):
        """Yield grid slices in a west direction."""
        for row in range(self.side):
            grid_slice = list()
            for col in range(self.side - 1, -1, -1):
                grid_slice.append(self.grid[row][col])
            yield grid_slice

    def _slices_east(self):
        """Yield grid slices in an east direction."""
        for row in range(self.side):
            grid_slice = list()
            for col in range(self.side):
                grid_slice.append(self.grid[row][col])
            yield grid_slice

    def _slices_north_west(self):
        """Yield grid slices in a north-west direction."""
        for diag in range(self.side + self.side - 1):
            grid_slice = list()
            for col in range(min(self.side, diag + 1) - 1, max(0, 1 - self.side + diag) - 1, -1):
                grid_slice.append(self.grid[col - diag + self.side - 1][col])
            yield grid_slice

    def _slices_north_east(self):
        """Yield grid slices in a north-east direction."""
        for diag in range(self.side + self.side - 1):
            grid_slice = list()
            for col in range(max(0, 1 - self.side + diag), min(self.side, diag + 1)):
                grid_slice.append(self.grid[diag - col][col])
            yield grid_slice

    def _slices_south_west(self):
        """Yield grid slices in a south-west direction."""
        for diag in range(self.side + self.side - 1):
            grid_slice = list()
            for col in range(min(self.side, diag + 1) - 1, max(0, 1 - self.side + diag) - 1, -1):
                grid_slice.append(self.grid[diag - col][col])
            yield grid_slice

    def _slices_south_east(self):
        """Yield grid slices in a south-east direction."""
        for diag in range(self.side + self.side - 1):
            grid_slice = list()
            for col in range(max(0, 1 - self.side + diag), min(self.side, diag + 1)):
                grid_slice.append(self.grid[col - diag + self.side - 1][col])
            yield grid_slice
