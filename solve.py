import argparse
import os
import random
import sys
from pathlib import Path
from typing import Optional


def print_bold(phrase: str, color: Optional[str] = None) -> None:
    colors = {'black': 0, 'red': 1, 'green': 2, 'yellow': 3, 'blue': 4, 'magenta': 5, 'cyan': 6, 'white': 7}
    os.system(f'tput bold; tput setaf {colors.get(color, 7)}; echo "{phrase}"; tput sgr0')


if __name__ == '__main__':
    file_ = Path(__file__)
    sys.path.append(file_.parent)
    from grid_builder import GridBuilder
    from utils import Bookworm
    from word_search import WordSearchSolver, WordTree

    parser = argparse.ArgumentParser(
        prog='../solve.py',

        usage=f'\n  python3 ../{file_.name}\n'
              f'\tGenerate a 15-character grid with none words hidden inside\n'
              f'\tand find all words read from the default dictionary.\n\n'
              f'  python3 ../{file_.name} -g 10 -w lumberjack cocoa helicopter\n '
              f'\tGenerate a 10-character grid with the specified words hidden inside.\n\n'
              f'  python3 ../{file_.name} -d `PATH_TO_A_TEXT_FILE`\n'
              f'\tGenerate a standard grid, but use a specified file to use as known words.\n\n'
              f'  python3 ../{file_.name} --show-dictionary\n'
              f'\t Show path to a standard program dictionary.\n\n'
              f'  python3 ../{file_.name} -q\n'
              f'\t Do not show the results until consent received.\n\n'
              f'  python3 ../{file_.name} -v\n'
              f'\t Show the all the words found in the grid in addition to the found words list.\n',

        description='Word Puzzle: a puzzle consisting of letters arranged in a grid '
                    'which contains a number of hidden words written in various directions. '
                    'This program lets you generate such puzzles with a specified `grid` size, '
                    'in which you can hide a reasonable number of words (optionally). '
                    'If no words specified, a completely random grid will be built'
                    ' (with some randomly selected words implanted). '
                    'The program comes with a 60_000+ dictionary of known words, but if you`d like to use '
                    'your own words dictionary, pass it as a `dictionary` argument'
    )
    parser.add_argument('-g', '--grid', type=int, default=15, help='Specify the grid size.')
    parser.add_argument('-w', '--words_to_hide', type=str, default=[], nargs='+', help='A space-delimited list of words '
                                                                                       'to hide inside the Word Puzzle grid.')
    parser.add_argument('-d', '--dictionary', type=str, default=None, help='Path to a custom word dictionary to be used.')
    parser.add_argument('-s', '--show-dictionary', action='store_true', help='Show the default word dictionary of known words.')
    parser.add_argument('-q', '--quiet', action='store_true', help='Skip showing the results. Show only the grid.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show all found words (by default, only hidden words shown).')
    cli_args = parser.parse_args()

    default_dictionary = file_.parent.joinpath('data/words.txt')
    if cli_args.show_dictionary:
        raise SystemExit(f'Default program dictionary is here: {default_dictionary}')
    known_words = Path(cli_args.dictionary).expanduser() if cli_args.dictionary else default_dictionary
    bookworm = Bookworm(data_file=known_words, longest_word=int(.9 * cli_args.grid))  # Using shorter words decreases number of collisions.
    words_to_hide = cli_args.words_to_hide or random.choices(bookworm.words, k=random.randint(3, 6))
    grid = GridBuilder(words_to_hide=words_to_hide, side=cli_args.grid)
    print(f'\n{grid}\n')

    solver = WordSearchSolver(word_tree=WordTree(bookworm.words))
    result = solver.solve(grid.grid)
    if cli_args.quiet:
        while True:
            answer = input('Show the results? (Y/N) ')
            if answer.lower() in ('y', 'yes'):
                break
    implanted = set(word for word in grid.implanted_words)
    found = set(w for w in result)
    if implanted.issubset(found):
        print_bold('ALL HIDDEN WORDS FOUND', color='green')
    print_bold('\nWORDS HIDDEN:')
    for word in sorted(implanted):
        print(word)
    print_bold('\nWORDS FOUND:')
    for word in sorted(found):
        if word in implanted:
            print(word)
    if cli_args.verbose:
        print_bold('\nREST OF THE WORDS FOUND IN THE GRID:')
        for word in sorted(found - implanted):
            print(word)
