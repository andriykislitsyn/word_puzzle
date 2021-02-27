import logging
import os
import random
import string
from typing import List, ClassVar, Tuple, Optional, Any, Union

from utils import compass


class GridBuilder:
    """
        Class building a Word Search puzzle grid.

        Attributes:
          words_to_hide - list of words we desire to hide inside the grid.
          side - length of the grid side.
          grid - the grid (2d matrix of letters).
          implanted_words - list of words that were hidden inside the grid.
    """
    placeholder: ClassVar[str] = '•'

    def __init__(self, words_to_hide: Optional[Union[List[str], str]] = None, side: int = 15):
        self.words_to_hide: List[str] = self.__process_input(words_to_hide)
        self.side: int = self.__check_side(side)
        self.grid: List[List[str]] = [[self.placeholder for _ in range(self.side)] for _ in range(self.side)]
        self.implanted_words: List[Tuple[str, Tuple[int, int], Tuple[int, int]]] = list()
        self.populate()

    def __repr__(self):
        return '\n'.join('  '.join(r) for r in self.grid)

    def populate(self) -> None:
        """Populate the grid with words provided in `words_to_hide` and fill the rest with random letters."""
        for word in self.words_to_hide:
            attempts_left = 100
            while attempts_left:
                if self.__implant_word(word):
                    self.implanted_words.append((word, self.__start_point, self.__finish_point))
                    break
                attempts_left -= 1
                if not attempts_left:
                    logging.error(f'Could not add "{word}"')
        self.__fill_empty_cells()

    def __implant_word(self, word: str, direction: int = compass.chose_random_direction()) -> bool:
        """Implant `word` into the grid based on the `direction` provided."""
        if len(word) > self.side:
            raise ValueError(f'"{word}" cannot be inserted into the grid due to its length.')
        positions = list()
        col, row = self.__find_starting_cell(word, direction)
        self.__start_point = col, row
        for char in word:
            if not (self.grid[row][col] in (self.placeholder, char)):
                return False
            positions.append((char, col, row))
            col, row = self.__find_next_cell(col, row, direction)
        self.__finish_point = positions[-1][1:]
        if len(positions) == len(word):
            for char, col, row in positions:
                self.grid[row][col] = char
        return True

    def __find_starting_cell(self, word: str, direction: int) -> Tuple[int, int]:
        """Locate a starting point for the `word`"""
        while True:
            col, row = random.randint(0, self.side - 1), random.randint(0, self.side - 1)
            if self.__prevent_wall_collisions(word, col, row, direction):
                if self.grid[row][col] in (self.placeholder, word[0]):
                    self.__start_point = (col, row)
                    return col, row

    def __prevent_wall_collisions(self, word: str, col: int, row: int, direction: int) -> bool:
        """Calculate the distance between the given point and a grid wall given the `direction`."""
        col_pass, row_pass = True, True
        if direction in compass.western_directions:
            col_pass = (col + 1) >= len(word)
        elif direction in compass.eastern_directions:
            col_pass = self.side - col >= len(word)
        if direction in compass.northern_directions:
            row_pass = (row + 1) >= len(word)
        elif direction in compass.southern_directions:
            row_pass = self.side - row >= len(word)
        return all((col_pass, row_pass))

    @staticmethod
    def __find_next_cell(col: int, row: int, direction: int) -> Tuple[int, int]:
        """Locate a next cell based on given position and `direction`."""
        move = {compass.north: (0, -1), compass.south: (0, 1), compass.west: (-1, 0), compass.east: (1, 0), compass.north_west: (-1, -1),
                compass.north_east: (1, -1), compass.south_west: (-1, 1), compass.south_east: (1, 1)}.get(direction)
        return col + move[0], row + move[1]

    def __fill_empty_cells(self) -> None:
        """Fill every cell with a placeholder value with an uppercase letter."""
        for row in self.grid:
            for index, char in enumerate(row):
                if char == self.placeholder:
                    row[index] = random.choice(string.ascii_uppercase)

    @staticmethod
    def __check_side(side):
        if not isinstance(side, int):
            raise ValueError('Please provide a valid number')
        if side < 5 or side > 50:
            raise ValueError("Uh oh, let's make it somewhat larger than 4 and less than 50")
        return abs(side)

    @staticmethod
    def __process_input(words: Any) -> List[str]:
        """Process the input `words` to produce a list to work with."""
        if words is None:
            return []
        if isinstance(words, str):
            if os.path.exists(words):
                with open(words) as container:
                    words = container.read().splitlines()
            else:
                words = words.split(' ')
        elif isinstance(words, tuple) or isinstance(words, list) or isinstance(words, set):
            words = words
        else:
            logging.error('Could not process the words')
            return []
        return [w.strip().upper() for w in words if w.isalpha()]
