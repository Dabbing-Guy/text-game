from typing import List
from enemies import Combatant, Player
import pathlib


class Game:

    def __init__(self, story_progress: int = 0, player: Player = None):
        self.story_progress = story_progress
        self.player: Player = player or Player(1, ["Punch"])

    @classmethod
    def from_save(cls, save_data: List[str]):
        """Create a game from a save file"""
        story_progress = int(save_data[0])
        player = Player(int(save_data[1]), save_data[2].split("~"))
        return cls(story_progress, player)

    def make_save(self, save_name: str):
        """Save the game"""
        game_dir = pathlib.Path(__file__).parent.parent
        save_dir = game_dir / "saves"
        save_dir.mkdir(exist_ok=True)
        save_file = save_dir / (save_name + ".save")
        save_data = f"{self.story_progress}\n{self.player.lvl}\n{'~'.join(self.player.skills)}"
        with save_file.open("w") as f:
            f.write(save_data)
