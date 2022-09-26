import time
import curses
from typing import List, Sequence, TypeVar, Tuple, Union, NoReturn
import game_class

DOWN_KEYS: Tuple[int, int, int] = (curses.KEY_DOWN, ord('j'), ord('s'))
RIGHT_KEYS: Tuple[int, int, int] = (curses.KEY_RIGHT, ord('l'), ord('d'))
UP_KEYS: Tuple[int, int, int] = (curses.KEY_UP, ord('k'), ord('w'))
LEFT_KEYS: Tuple[int, int, int] = (curses.KEY_LEFT, ord('h'), ord('a'))


def print_center(string: str,
                 line: int,
                 stdscr: curses.window,
                 color: int = curses.A_NORMAL):
    """Prints a string centered on the screen. Fails if the string is longer than the screen"""
    stdscr.addstr(line,
                  stdscr.getmaxyx()[1] // 2 - len(string) // 2, string, color)


def error_screen(error: str, stdscr: curses.window):
    """Prints an error message"""
    stdscr.clear()
    print_center(error, curses.LINES // 2, stdscr, curses.A_STANDOUT)
    stdscr.getch()


def clear_input(stdscr: curses.window):
    """
        Clear stdin buffer so getch() pauses until user input.
        """
    stdscr.nodelay(True)
    while stdscr.getch() != curses.ERR:
        continue
    stdscr.nodelay(False)


def _get_attribute(char: str, stdscr: curses.window) -> int:
    """Gets the curses attribute for a given attribute code"""
    if char == "b": return curses.A_BOLD
    if char == "i": return curses.A_ITALIC
    if char == "u": return curses.A_UNDERLINE
    if char == "n": return curses.A_NORMAL
    error_screen("Invalid attribute tag", stdscr)
    return curses.A_NORMAL


def input_screen(prompt: str) -> str:
    """Gets a string input from the user"""
    size_y = 3
    size_x = len(prompt) + curses.COLS // 2
    begin_y: int = curses.LINES // 2 - size_y // 2
    begin_x: int = curses.COLS // 2 - size_x // 2
    inputscr = curses.newwin(size_y, size_x, begin_y, begin_x)

    inputscr.box()
    inputscr.addstr(1, 1, prompt)
    a = inputscr.getstr(1,
                        len(prompt) + 1,
                        size_x - len(prompt) - 2).decode("utf-8")
    inputscr.clear()
    inputscr.refresh()
    return a


def valid_int_input(lower_limit: int,
                    upper_limit: int,
                    scr: curses.window,
                    prompt: str = "> ") -> int:
    """Get a valid int input
    lower_limit and upper_limit are inclusive"""
    while True:
        scr.addstr(prompt)
        curses.echo()
        user_input = scr.getstr()
        try:
            as_num = int(user_input)
        except ValueError:
            # Was not an int
            continue
        if not lower_limit <= as_num <= upper_limit:
            # Does not fit between upper and lower limit
            continue
        curses.noecho()
        return as_num


T = TypeVar("T")


def menu(options: Sequence[T],
         prompt: str,
         prompt_attr: int = curses.A_BOLD) -> T:
    """Lets the user choose from a selection of options, returns the chosen option"""
    str_options: List[str] = list(map(str, options))
    all_menu_things: List[str] = [prompt] + str_options

    curses.update_lines_cols()
    size_y: int = len(options) + 3
    size_x: int = len(max(all_menu_things, key=len)) + 6
    begin_y: int = curses.LINES // 2 - size_y // 2
    begin_x: int = curses.COLS // 2 - size_x // 2
    menuscr = curses.newwin(size_y, size_x, begin_y, begin_x)
    menuscr.keypad(True)
    curses.curs_set(0)
    # From before I knew about scr.box
    """
    textpad.rectangle(stdscr, begin_y - 1, begin_x - 1, begin_y + size_y + 1,
                      begin_x + size_x + 1)
                      """

    # Selection cycle
    selected: int = 0
    while True:
        index: int
        item: str
        for index, item in enumerate(str_options):
            if index == selected:
                print_center(item, index + 1 + 1, menuscr, curses.A_REVERSE)
                continue
            print_center(item, index + 1 + 1, menuscr)
        menuscr.box()
        print_center(prompt, 1, menuscr, prompt_attr)
        key: int = menuscr.getch()
        if key in UP_KEYS and selected > 0:
            selected -= 1
        elif key in DOWN_KEYS and selected < len(str_options) - 1:
            selected += 1
        elif key == ord("\n") or key == ord(" "):
            menuscr.clear()
            menuscr.refresh()
            return options[selected]

        menuscr.refresh()


def escape_menu(game: game_class.Game) -> Union[None, NoReturn]:
    """Escape menu"""
    options: List[str] = ["Resume", "Save", "Exit"]
    option: str = menu(options, "Escape Menu")
    if option == "Save":
        curses.echo()
        curses.curs_set(1)
        save_name: str = input_screen("Save Name: ")
        curses.noecho()
        curses.curs_set(0)
        game.make_save(save_name)
        return escape_menu(game)
    elif option == "Exit":
        exit()
    elif option == "Resume":
        return None
    raise ValueError("io_functs.menu returned a value it shouldn't have")


def story_print(text: str, stdscr: curses.window, game: Union[game_class.Game,
                                                              None]):
    """Prints a story message. `game` is needed for the escape menu.
    Accepts in-text attribute delcarations. A attribute is started with \` (without the backslash) and then the attribute character.
    Available attributes:
    \`b - bold
    \`i - italic
    \`u - underline
    \`n - normal"""
    stdscr.clear()
    # TODO: Implement attribute tags
    attribute_delcaration: bool = False
    attribute: int = curses.A_NORMAL
    for char in text:
        if char == "`":
            attribute_delcaration = True
            continue
        if attribute_delcaration:
            attribute = _get_attribute(char, stdscr)
            attribute_delcaration = False
            continue
        stdscr.addch(char, attribute)
        stdscr.refresh()
        time.sleep(0.02)
    stdscr.addch('\n')
    clear_input(stdscr)
    # Blinking dots effect
    curses.halfdelay(7)
    while True:
        stdscr.addstr("...")
        key = stdscr.getch()
        if key in [27, ord('q')] and not game is None:
            # Escape or q was pressed, display escape menu
            escape_menu(game)
            y, x = stdscr.getyx()
            stdscr.move(y, x - 3)
            continue

        if key != curses.ERR:
            break
        y, x = stdscr.getyx()
        stdscr.move(y, x - 3)
        stdscr.clrtoeol()
        stdscr.refresh()
        if stdscr.getch() != curses.ERR:
            break
    curses.cbreak()
