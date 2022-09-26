from pathlib import Path
import curses
import curses.textpad as textpad
from typing import NoReturn, Sequence, Any, List, Tuple, Union, TypeVar
import io_functs
from io_functs import story_print, menu, escape_menu
import game_class
import maps
import enemies

DOWN_KEYS: Tuple[int, int, int] = (curses.KEY_DOWN, ord('j'), ord('s'))
RIGHT_KEYS: Tuple[int, int, int] = (curses.KEY_RIGHT, ord('l'), ord('d'))
UP_KEYS: Tuple[int, int, int] = (curses.KEY_UP, ord('k'), ord('w'))
LEFT_KEYS: Tuple[int, int, int] = (curses.KEY_LEFT, ord('h'), ord('a'))


def load_game_menu(stdscr: curses.window) -> game_class.Game:
    """Menu for loading a game"""
    game_dir = Path(__file__).parent.parent
    save_dir = game_dir / "saves"
    save_dir.mkdir(exist_ok=True)
    save_files: List[Path] = list(save_dir.glob("*.save"))
    if not save_files:
        io_functs.error_screen("No save files found.", stdscr)
        return main(stdscr)
    save_names: List[str] = [save_file.stem for save_file in save_files]
    save_name: str = io_functs.menu(save_names, "Load Save")
    save_file: Path = save_dir / (save_name + ".save")
    with save_file.open("r") as f:
        save_data: List[str] = f.readlines()
    return game_class.Game.from_save(save_data)


def battle_menu(enemies: List[enemies.Combatant], game: game_class.Game,
                stdscr: curses.window) -> None:
    while enemies:
        action = menu(game.player.skills, "Choose an action")
        enemy = menu(enemies, "Choose an enemy")
        player_turns = game.player.turns

        while player_turns > 0:
            if action == "Punch":
                story_print(game.player.punch(enemy), stdscr, game)
            elif action == "Sword Strike":
                story_print(game.player.sword_strike(enemy), stdscr, game)

            if enemy.hp <= 0:
                story_print(f"{enemy.name} has been defeated!", stdscr, game)
                enemies.remove(enemy)
            player_turns -= 1

        for enemy in enemies:
            enemy_turns = enemy.turns
            while enemy_turns > 0:
                story_print(enemy.attack(game.player), stdscr, game)
                if game.player.hp <= 0:
                    story_print("You have been defeated!", stdscr, game)
                    return
                story_print(f"You have {game.player.hp} HP left.", stdscr,
                            game)
                enemy_turns -= 1


def find_new_pos(game: game_class.Game, map: maps.Map, mapscr: curses.window,
                 key: int, pos: List[int]) -> List[int]:
    """Gets input and returns new player position
    [2] is 1 if the player is on interactable 1 tile, -1 if player is on exit tile, 0 otherwise"""
    old_pos = pos.copy()
    if key == ord("q") or key == 27:
        escape_menu(game)
        mapscr.redrawwin()
    elif key in DOWN_KEYS and pos[0] < map.LINES - 1:
        pos[0] += 1
    elif key in RIGHT_KEYS and pos[1] < map.COLS - 1:
        pos[1] += 1
    elif key in UP_KEYS and pos[0] > 0:
        pos[0] -= 1
    elif key in LEFT_KEYS and pos[1] > 0:
        pos[1] -= 1

    if map.get_metamap_char(pos) == "#":
        # User moved into a wall, so don't move them
        return old_pos
    # pos[2] is used to tell main if the player moved into a special zone
    elif map.get_metamap_char(pos) == "%":
        pos[2] = 1
    elif map.get_metamap_char(pos) == "e":
        pos[2] = -1
    elif map.get_metamap_char(pos) == " ":
        pos[2] = 0
    return pos


def main(stdscr: curses.window):
    """Main menu"""
    curses.curs_set(0)
    while curses.LINES < 25 or curses.COLS < 85:
        story_print(
            "Please resize your terminal to at least 25 lines and 85 columns.",
            stdscr, None)
        curses.update_lines_cols()
    stdscr.clear()
    options: List[str] = ["New Game", "Load Save", "Exit"]
    option: str = io_functs.menu(options, "Main Menu")
    if option == "Exit": exit()
    elif option == "New Game": game = game_class.Game()
    elif option == "Load Save": game = load_game_menu(stdscr)
    PLAYER: str = "@"
    while True:
        if game.story_progress == 0:
            # Intro
            story_print(
                "You wake up. The ground is hard. You open your eyes and see that you are in a cave. ",
                stdscr, game)
            story_print(
                "`iWhy am I in a cave? `nyou think to yourself. You try your best to remember how you got there.",
                stdscr, game)
            story_print("You think back to that the last thing you remember.",
                        stdscr, game)
            story_print(
                "You were standing in the subway station, waiting for your train home.",
                stdscr, game)
            story_print(
                "As the train started to pull into the station, someone shoved you forward, off the platform.",
                stdscr, game)
            story_print("The train instantly killed you.", stdscr, game)
            story_print("`bYou were murdered.", stdscr, game)
            story_print(
                "As this realization sinks in, you look around in the cave you are sitting in.",
                stdscr, game)
            stdscr.clear()
            stdscr.refresh()
            game.story_progress += 1
            game.make_save("autosave")
        elif game.story_progress == 1:
            # Cave exploration
            curses.update_lines_cols()
            current_map: maps.Map = maps.Map.from_name("cave")
            mapy = curses.LINES // 2 - current_map.LINES // 2
            mapx = curses.COLS // 2 - current_map.COLS // 2
            mapscr = curses.newwin(current_map.LINES, current_map.COLS, mapy,
                                   mapx)
            mapscr.addstr(current_map.as_str)
            mapscr.keypad(True)
            pos: List[int] = list(current_map.get_starting_pos())

            while True:
                # Draw player
                mapscr.addch(pos[0], pos[1], PLAYER, curses.A_BOLD)
                mapscr.refresh()
                # Input
                key = mapscr.getch()
                # Delete old player
                mapscr.addch(pos[0], pos[1],
                             current_map.as_list[pos[0]][pos[1]])
                # Figure out player's new position
                pos = find_new_pos(game, current_map, mapscr, key, pos)
                if pos[2] == 1:
                    choice = io_functs.menu(
                        ["Pick up the sword", "Leave it"],
                        "You see a sword on the ground. What do you do?")
                    if choice == "Pick up the sword":
                        current_map = maps.Map.from_name("cave_no_sword")
                        mapscr.addstr(0, 0, current_map.as_str)
                        game.player.skills.append("Sword Strike")
                        if io_functs.menu(
                            ["Great!", "idk that sounds pretty mid"],
                                "You gained a new skill: Sword Strike!"
                        ) == "idk that sounds pretty mid":
                            io_functs.menu(["Continue"], "Be Greatful")
                    mapscr.redrawwin()
                if pos[2] == -1:
                    mapscr.clear()
                    game.story_progress += 1
                    game.make_save("autosave")
                    break
        elif game.story_progress == 2:
            # After getting out of the cave
            io_functs.story_print(
                "As you walk out of the cave, you find yourself in a forest.",
                stdscr, game)
            io_functs.story_print(
                "As you are looking around, you stuble upon a small group of 3 slimes.",
                stdscr, game)
            io_functs.story_print("Or at least that is what they look like.",
                                  stdscr, game)
            io_functs.story_print("`iI guess I am in a different world now.",
                                  stdscr, game)
            io_functs.story_print(
                "As you look at the slimes, you prepare for battle.", stdscr,
                game)
            stdscr.clear()
            stdscr.refresh()
            game.story_progress += 1
            game.make_save("autosave")
        elif game.story_progress == 3:
            # Slime battle
            slimes: List[enemies.Combatant] = [
                enemies.Slime(1, num + 1) for num in range(3)
            ]
            battle_menu(slimes, game, stdscr)
            game.story_progress += 1
            game.make_save("autosave")
        else:
            story_print(
                "To be continued... (This is all the game content I have developed so far)",
                stdscr, game)
            return


if __name__ == "__main__":
    curses.wrapper(main)
