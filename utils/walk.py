import curses

# for walking in the dungeon


def main(stdscr):
    curses.noecho()          # keys deactivation
    curses.cbreak()          # characters deactivation
    stdscr.keypad(True)      # arrows activation

    while True:
        c = stdscr.getch()   # instant reading of a key

        if c == curses.KEY_UP:
            stdscr.addstr("N\n")
        elif c == curses.KEY_DOWN:
            stdscr.addstr("S\n")
        elif c == curses.KEY_LEFT:
            stdscr.addstr("W\n")
        elif c == curses.KEY_RIGHT:
            stdscr.addstr("E\n")
        elif c == 27:  # Esc
            break

    # parameters restauration
    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(main)
