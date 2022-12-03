from typing import Callable, List, Tuple, Any

from codebase.tinyisland.Tile import TileData, TileType, Position, AdjacencyInfo

HOUSES_REWARD_PER_UNIQUE_TYPE_NEARBY= 2

class Board:
    def __init__(self, col_num: int, row_num: int):
        self.col_num = col_num
        self.row_num = row_num
        self.tile_map = dict()
        for r in range(row_num):
            for c in range(col_num):
                pos = Position(c, r)
                adj_info = self._generate_adjacency_info(pos)
                self.tile_map[pos] = TileData(pos, adj_info)

    def _generate_adjacency_info(self, pos: Position) -> AdjacencyInfo:
        """
        Helper Method for generating valid adjacency info.
        param pos: A tuple of two ints representing the position from which to generate adjacency info.
        :return: A tuple of two list of ints representing touching tiles and nearby tiles.
        """
        pos_x, pos_y = pos.col, pos.row
        adj, near, col, row = [], [], [], []
        if pos_x < self.col_num - 1:
            adj.append(Position(pos_x + 1, pos_y))
        if pos_x > 0:
            adj.append(Position(pos_x - 1, pos_y))
        if pos_y < self.row_num - 1:
            adj.append(Position(pos_x, pos_y + 1))
        if pos_y > 0:
            adj.append(Position(pos_x, pos_y - 1))
        if pos_x < self.col_num - 1 and pos_y < self.row_num - 1:
            near.append(Position(pos_x + 1, pos_y + 1))
        if pos_x < self.col_num - 1 and pos_y > 0:
            near.append(Position(pos_x + 1, pos_y - 1))
        if pos_x > 0 and pos_y < self.row_num - 1:
            near.append(Position(pos_x - 1, pos_y + 1))
        if pos_x > 0 and pos_y > 0:
            near.append(Position(pos_x - 1, pos_y - 1))
        for r in range(self.row_num - 1):
            if r != pos_y:
                col.append(Position(pos_x, r))
        for c in range(self.col_num - 1):
            if c != pos_x:
                row.append(Position(pos_y, c))
        return AdjacencyInfo(adj, near, col, row)

    def _get_tile_at_position(self, pos: Position) -> TileData:
        """
        Helper getter method for single tile data.
        param pos: A tuple of two ints representing the position (COORDINATES).
        :return: TileData at the coordinate. Throws an Exception if the coordinate is outside the board.
        """
        x, y = pos.col, pos.row
        if x < 0 or y < 0 or x >= self.col_num or y >= self.row_num:
            raise ValueError("Position Outside Board Dimensions")
        return self.tile_map[pos]

    def _get_tiles_at_positions(self, lo_pos: List[Position]) -> List[TileData]:
        """
        param lo_pos: A list of tuples of two ints representing the position (COORDINATES).
        :return: A list of TileData
        """
        lo_tiles = []
        for pos in lo_pos:
            lo_tiles.append(self._get_tile_at_position(pos))
        return lo_tiles

    def _get_score_at_position(self, tile_position: Position) -> int:
        tar_tile = self._get_tile_at_position(tile_position)
        if tar_tile.type == TileType.HOUSES:
            return self._get_score_helper_houses(tar_tile)
        elif tar_tile.type == TileType.CHURCHES:
        elif tar_tile.type == TileType.FOREST:
        elif tar_tile.type == TileType.MOUNTAIN:
        elif tar_tile.type == TileType.SAND:
        elif tar_tile.type == TileType.BOATS:
        elif tar_tile.type == TileType.WAVES:
        else:
            return 0

    def _get_score_helper_houses(self, tile: TileData):
        matches = 0
        lo_unique_types = list()
        for near_pos in (tile.adj_info.adj + tile.adj_info.near):
            tar_tile = self._get_tile_at_position(near_pos)
            tar_type = tar_tile.type
            if tar_type not in lo_unique_types and tar_type != TileType.EMPTY:
                matches += 1
                lo_unique_types.append(tar_type)
        return HOUSES_REWARD_PER_UNIQUE_TYPE_NEARBY * matches

    def _validate_all_tiles_and_compute_penalties(self) -> int:
        penalty = 0
        for tile_pos in self.tile_map.keys():
            tile = self._get_tile_at_position(tile_pos)
            if (tile.type)

    def add_tile_type(self, tile_type: TileType, pos: Position):
        tile = self._get_tile_at_position(pos)
        if tile.is_occupied:
            raise ValueError("Tile Has Been Occupied")
        tile.add_type(tile_type)

    def get_score(self):
        score = 0 - self._validate_all_tiles_and_compute_penalties()
        score = 0
        for tile_pos in self.tile_map.keys():
            score += self._get_score_at_position(tile_pos)
        return score

    def view_board_cli(self):
        for r in range(self.row_num):
            row_str = ""
            for c in range(self.col_num):
                row_str += "   " + self._get_tile_at_position(Position(c, r)).type.value
            print(row_str + "\n")