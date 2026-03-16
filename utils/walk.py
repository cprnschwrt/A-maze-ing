import curses

def main(stdscr):
    # Terminal config
    curses.noecho()          # Keys deactivation
    curses.cbreak()          # Characters deactivation
    stdscr.keypad(True)      # Arrows activation

    while True:
        c = stdscr.getch()   # Instant reading of a key

        if c == curses.KEY_UP:
            stdscr.addstr("N\n")
        elif c == curses.KEY_DOWN:
            stdscr.addstr("S\n")
        elif c == curses.KEY_LEFT:
            stdscr.addstr("W\n")
        elif c == curses.KEY_RIGHT:
            stdscr.addstr("E\n")
        elif c == 27:  # Esc Key
            break

    # Parameters restauration
    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)
