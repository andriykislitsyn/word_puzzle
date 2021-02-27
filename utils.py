import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


class BookWorm:
    """
        Class reading words provided in a text file.

        Attributes:
          data_file - path to a file with known words.
          longest_word - max length of a word we want to keep.
    """
    __slots__ = ('data_file', 'longest_word', '__words')

    def __init__(self, data_file: Path, longest_word: Optional[int] = None):
        self.data_file = data_file
        self.longest_word = longest_word or 255
        self.__words: List[str] = list()

    @property
    def words(self) -> List[str]:
        if self.__words:
            return self.__words
        with open(self.data_file) as data_file:
            return [word.upper() for word in data_file.read().splitlines() if len(word) <= self.longest_word]


@dataclass(frozen=True)
class Compass:
    """Dataclass containing directions used for navigation and orientation inside the grid."""
    north = 0
    south = 1
    west = 2
    east = 3
    north_east = 5
    north_west = 4
    south_west = 6
    south_east = 7

    northern_directions = (north, north_west, north_east)
    southern_directions = (south, south_west, south_east)
    western_directions = (west, north_west, south_west)
    eastern_directions = (east, north_east, south_east)
    directions = tuple(set(northern_directions + southern_directions + western_directions + eastern_directions))

    def as_str(self, direction: int):
        """Return human readable name of the direction."""
        return {self.north: 'N', self.south: 'S', self.west: 'W', self.east: 'E',
                self.north_west: 'NW', self.north_east: 'NE', self.south_west: 'SW', self.south_east: 'SE'}.get(direction)

    def chose_random_direction(self):
        """Select a random direction from all available."""
        return random.choice(self.directions)


compass = Compass()
