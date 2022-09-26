from pathlib import Path
from typing import List


class Map:

    def __init__(self, _map: List[str], _map_data: List[str]):
        self._map: List[str] = _map
        self._map_data: List[str] = _map_data
        self.COLS: int = len(self._map[0]) + 1
        self.LINES: int = len(self._map) + 1
        if not self.COLS == len(self._map_data[0]) + 1:
            raise ValueError("Map and map data are not the same size.")
        if not self.LINES == len(self._map_data) + 1:
            raise ValueError("Map and map data are not the same size.")

    @property
    def as_str(self) -> str:
        return "\n".join(self._map)

    @property
    def as_list(self) -> List[str]:
        return self._map

    def get_starting_pos(self) -> List[int]:
        for y, line in enumerate(self._map_data):
            for x, char in enumerate(line):
                if char == "S":
                    return [y, x, 0]
        raise ValueError("No starting position found.")

    def get_metamap_char(self, pos: List[int]) -> str:
        return self._map_data[pos[0]][pos[1]]

    @classmethod
    def from_files(cls, map_path: Path, map_data_path: Path):
        with open(map_data_path, "r") as f2:
            with open(map_path, "r") as f:
                return cls(f.read().splitlines(), f2.read().splitlines())

    @classmethod
    def from_list(cls, map: List[str], map_data: List[str]):
        return cls(map, map_data)

    @classmethod
    def from_name(cls, map_name: str):
        """Looks for a .map and .mapdata file with the name given in the maps folder"""
        game_dir = Path(__file__).parent.parent
        map_dir = game_dir / "maps"
        return cls.from_files(map_dir / f"{map_name}.map",
                              map_dir / f"{map_name}.mapdata")
