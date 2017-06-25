import curses
from curses import wrapper

MAP = """###################################X#
# #       #       #     #         # #
# # ##### # ### ##### ### ### ### # #
#       #   # #     #     # # #   # #
##### # ##### ##### ### # # # ##### #
#   # #       #     # # # # #     # #
# # ####### # # ##### ### # ##### # #
# #       # # #   #     #     #   # #
# ####### ### ### # ### ##### # ### #
#     #   # #   # #   #     # #     #
# ### ### # ### # ##### # # # ##### #
#   #   # # #   #   #   # # #   #   #
####### # # # ##### # ### # ### ### #
#     # #     #   # #   # #   #     #
# ### # ##### ### # ### ### ####### #
# #   #     #     #   # # #       # #
# # ##### # ### ##### # # ####### # #
# #     # # # # #     #       # #   #
# ##### # # # ### ##### ##### # #####
# #   # # #     #     # #   #       #
# # ### ### ### ##### ### # ##### # #
# #         #     #       #       # #
#X###################################"""

inpits = {curses.KEY_UP: "Up",
          curses.KEY_DOWN: "Down"}

def main(stdscr):
    stdscr.clear()
    while True:
        # Store the key value in the variable `c`
        c = stdscr.getch()
        # Clear the terminal
        stdscr.clear()
        if c in inpits:
            stdscr.addstr(inpits[c])
        else:
            stdscr.addstr("Nope")

# wrapper is a function that does all of the setup and teardown, and makes sure
# your program cleans up properly if it errors!
wrapper(main)