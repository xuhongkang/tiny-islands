from enum import Enum
from typing import List


class TileType(Enum):
    EMPTY = "E"
    HOUSES = "H"
    CHURCHES = "C"
    FOREST = "F"
    MOUNTAIN = "M"
    BOATS = "B"
    WAVES = "W"
    BEACHES = "S"


ON_ISLAND_TILE_TYPES = [TileType.HOUSES, TileType.CHURCHES, TileType.FOREST, TileType.MOUNTAIN]
ON_SHORE_TILE_TYPES = [TileType.BEACHES]
OFF_SHORE_TILE_TYPES = [TileType.BOATS, TileType.WAVES]
OFF_ISLAND_TILE_TYPES = ON_SHORE_TILE_TYPES + OFF_SHORE_TILE_TYPES


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
                 is_tile_on_island: bool = False, is_tile_on_shore: bool = False,
                 type_of_terrain: TileType = TileType.EMPTY, is_valid: bool = True):
        self.pos = position_on_board
        self.adj_info = adjacency_info
        self.is_occupied = is_tile_occupied
        self.on_island = is_tile_on_island
        self.on_shore = is_tile_on_shore
        self.type = type_of_terrain
        self.is_valid = is_valid

    def add_type(self, tar: TileType):
        """
        Adds the given type to the current tile data
        as well as Automatic Validation (For Lenient Total Score)
        """
        if tar == TileType.EMPTY:
            raise ValueError("Placing Empty TileData Type")
        elif tar in OFF_ISLAND_TILE_TYPES and self.on_island:
            self.is_valid = False
        self.type = tar
        self.is_occupied = True

    def mark_as_island(self):
        """
        Method Used To Update The Tile Type when marked as island
        as well as Automatic Validation (For Lenient Total Score)
        """
        self.on_island = True
        if self.type in OFF_ISLAND_TILE_TYPES:
            self.is_valid = False

    def mark_as_shore(self):
        """
        Method Used To Update Tile Type when marked as shore
        as well as Automatic Validation (For Lenient Total Score)
        """
        self.on_shore = True
        if self.type in ON_ISLAND_TILE_TYPES:
            self.is_valid = False

    def validate_tile_type(self):
        """
        Method Used To Validate Tile Types At the End Of the Game (For a Strict Total Score)
        """
        if self.type in ON_ISLAND_TILE_TYPES:
            self.is_valid = self.on_island
        elif self.type in OFF_ISLAND_TILE_TYPES:
            self.is_valid = not self.on_island
