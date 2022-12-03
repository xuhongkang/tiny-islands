from enum import Enum
from typing import Callable, List, Tuple, Any


class TileType(Enum):
    EMPTY = "E"
    HOUSES = "H"
    CHURCHES = "C"
    FOREST = "F"
    MOUNTAIN = "M"
    BOATS = "B"
    WAVES = "W"
    SAND = "S"


class Position:
    def __init__(self, column_index: int, row_index: int):
        self.col = column_index
        self.row = row_index


class AdjacencyInfo:
    def __int__(self, adjacent_pos: List[Position], near_pos: List[Position],
                col_pos: List[Position], row_pos: List[Position]):
        self.adj = adjacent_pos
        self.near = near_pos
        self.col = col_pos
        self.row = row_pos


class TileData:
    """
    A tile contains position, and a tuple of two list of ints representing touching tiles and nearby tiles.
    """

    def __init__(self, position_on_board: Position, adjacency_info: AdjacencyInfo, is_tile_occupied: bool = False,
                 is_tile_on_island: bool = False, type_of_terrain: TileType = TileType.EMPTY, is_valid: bool = True):
        self.pos = position_on_board
        self.adj_info = adjacency_info
        self.is_occupied = is_tile_occupied
        self.on_island = is_tile_on_island
        self.type = type_of_terrain
        self.is_valid = is_valid

    def add_type(self, tar: TileType):
        """
        Setter method for a tile data.
        param tar: Enum of Tile types. Throws an exception if type EMPTY
        """
        if tar == TileType.EMPTY:
            raise ValueError("Placing Empty TileData Type")
        self.type = tar
        self.is_occupied = True

    def make_as_island(self):
        self.on_island = True

    def validate_for_turn(self, result: bool):
        self.is_valid = result


