# Text Game

This program is a basic text game with map exploration, turn based combat, a basic isekai story, menus, and a save system. It uses the Python curses library for io. 

## State of the game now

Right now the game is lacking content. It wouldn't be very hard to add more story and content (due to all of the already written functions), but I don't have the time to invest in making more content. The save system is also quite rudimentry.

## To Run

1. `pip install .` to install dependencies (currently optional on platforms that have the Python curses module by default)
2. `python src/main.py` or `python src\main.py` depending on which platform you are on

## Notable Features

- You can use q or esc to open an escape menu at almost any in the game except when in a menu.
- For going down up left right, you can use wasd, vim movement keys, or the arrow keys. To select a item in the menu, use enter
- Mostly static typed
