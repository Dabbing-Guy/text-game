import curses


def main(stdscr: curses.window):
    mypad = curses.newpad(3000, 1000)
    for iteration in range(50):
        mypad.addstr("-------------------\n")
        for line in range(iteration + 1):
            for col in range(iteration + 1):
                i = 1
                mypad.addstr(str(i + line + col).rjust(3))
            mypad.addch("\n")
    y = 0
    curses.curs_set(0)
    mypad.keypad(True)
    mypad.refresh(y, 0, 0, 0, curses.LINES - 1, curses.COLS - 1)
    while True:
        mypad.refresh(y, 0, 0, 0, curses.LINES - 1, curses.COLS - 1)
        key = mypad.getch()
        if key == ord("q"):
            break
        if key == curses.KEY_UP and y > 0:
            y -= 1
        if key == curses.KEY_DOWN:
            y += 1


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except curses.error:
        print("Your terminal is too small to run this program.")
        exit(1)
