import argparse
import random
import sys
from pathlib import Path


if __name__ == '__main__':
    file_ = Path(__file__)
    sys.path.append(file_.parent)
    from grid_builder import GridBuilder
    from utils import BookWorm
    from word_search import WordSearchSolver

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
              f'\t Do not show the results until consent received.\n',

        description='Word Puzzle: a puzzle consisting of letters arranged in a grid '
                    'which contains a number of hidden words written in various directions.'
                    'This program lets you generate such puzzles with specified `grid` sizes,'
                    'you can hide some number of words inside your grid (optionally). '
                    'Otherwise, a completely random grid will be built.'
                    'The program comes with a 60_000+ known words, if you like to use'
                    'your own words dictionary, pass it as `dictionary` argument'
    )
    parser.add_argument('-g', '--grid', type=int, default=15, help='Specify the grid size.')
    parser.add_argument('-w', '--words_to_hide', type=str, default=[], nargs='+', help='A space-delimited list of words '
                                                                                       'to hide inside the Word Puzzle grid.')
    parser.add_argument('-d', '--dictionary', type=str, default=None, help='Path to a custom word dictionary to be used.')
    parser.add_argument('-s', '--show-dictionary', action='store_true', help='Show the default word dictionary of known words.')
    parser.add_argument('-q', '--quiet', action='store_true', help='Skip showing the results. Show only the grid.')
    cli_args = parser.parse_args()

    default_dictionary = file_.parent.joinpath('data/words.txt')
    if cli_args.show_dictionary:
        raise SystemExit(f'Default program dictionary is here: {default_dictionary}')
    known_words = Path(cli_args.dictionary).expanduser() if cli_args.dictionary else default_dictionary

    book_worm = BookWorm(data_file=known_words, longest_word=int(.9 * cli_args.grid))  # Using bit shorter words decreases number of collisions
    words_to_hide = cli_args.words_to_hide or random.choices(book_worm.words, k=random.randint(3, 6))
    grid = GridBuilder(words_to_hide=words_to_hide, side=cli_args.grid)
    print(f'\n{grid}\n')

    solver = WordSearchSolver(book_worm.words)
    result = solver.solve(grid.grid)
    if cli_args.quiet:
        while True:
            answer = input('Show the results? (Y/N) ')
            if answer.lower() in ('y', 'yes'):
                break
    implanted = set(word for word in grid.implanted_words)
    print('WORDS HIDDEN:')
    for word in sorted(implanted):
        print(word)
    found = set(w for w in result)
    print('\nWORDS FOUND:')
    for word in sorted(found):
        if word in implanted:
            print(word)
    if implanted.issubset(found):
        print('\nALL HIDDEN WORDS FOUND\n')
