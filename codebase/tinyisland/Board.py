from typing import List

from Tile import Position, TileData, AdjacencyInfo, TileType, ON_ISLAND_TILE_TYPES

PENALTY_PER_INVALID_TILE = -5
HOUSES_REWARD_PER_UNIQUE_TYPE_NEARBY = 2
CHURCHES_REWARD_PER_HOUSES_NEARBY = 2
CHURCHES_REWARD_PER_OTHER_HOUSES_ON_ISLAND = 1
FOREST_REWARD_PER_FOREST_ADJACENT = 1
MOUNTAIN_REWARD_PER_FOREST_NEARBY = 2
BEACHES_REWARD_IF_ON_SHORE = 1
WAVES_REWARD_IF_UNIQUE_COLUMN_ROW = 2


class Board:
    def __init__(self, col_num: int = 9, row_num: int = 9):
        self.col_num = col_num
        self.row_num = row_num
        self.tile_map = dict()
        self.islands = []
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
        if not tar_tile.is_valid:
            return PENALTY_PER_INVALID_TILE
        elif tar_tile.type == TileType.HOUSES:
            return self._get_score_helper_houses(tar_tile)
        elif tar_tile.type == TileType.CHURCHES:
            return self._get_score_helper_church(tar_tile)
        elif tar_tile.type == TileType.FOREST:
            return self._get_score_helper_forest(tar_tile)
        elif tar_tile.type == TileType.MOUNTAIN:
            return self._get_score_helper_mountain(tar_tile)
        elif tar_tile.type == TileType.BEACHES:
            return BEACHES_REWARD_IF_ON_SHORE if tar_tile.on_shore else 0
        elif tar_tile.type == TileType.BOATS:
            return self._get_score_helper_boats(tar_tile)
        elif tar_tile.type == TileType.WAVES:
            return self._get_score_helper_mountain(tar_tile)
        else:
            return 0

    def _get_score_helper_houses(self, tile: TileData):
        matches = 0
        lo_unique_types = list()
        for near_pos in (tile.adj_info.adj + tile.adj_info.near):
            tar_tile = self._get_tile_at_position(near_pos)
            tar_type = tar_tile.type
            if tar_type not in lo_unique_types and tar_type != TileType.EMPTY and tar_tile.is_valid:
                matches += 1
                lo_unique_types.append(tar_type)
        return HOUSES_REWARD_PER_UNIQUE_TYPE_NEARBY * matches

    def _get_score_helper_church(self, tile: TileData):
        island_tiles = []
        score = 0
        for island in self.islands:
            if tile.pos in island:
                island_tiles.extend(island)
        for near_pos in (tile.adj_info.adj + tile.adj_info.near):
            tar_tile = self._get_tile_at_position(near_pos)
            tar_type = tar_tile.type
            if tar_type == TileType.HOUSES and tar_tile.is_valid:
                score += CHURCHES_REWARD_PER_HOUSES_NEARBY
                if tar_tile.pos in island_tiles:
                    island_tiles.remove(tar_tile)
        for other_tile in island_tiles:
            if other_tile == TileType.CHURCHES:
                return 0
            elif other_tile == TileType.HOUSES:
                score += CHURCHES_REWARD_PER_OTHER_HOUSES_ON_ISLAND
        return score

    def _get_score_helper_forest(self, tile: TileData):
        matches = 0
        for adj_pos in tile.adj_info.adj:
            tar_tile = self._get_tile_at_position(adj_pos)
            tar_type = tar_tile.type
            if tar_type == TileType.FOREST and tar_tile.is_valid:
                matches += 1
        return FOREST_REWARD_PER_FOREST_ADJACENT * matches

    def _get_score_helper_mountain(self, tile: TileData):
        matches = 0
        for near_pos in (tile.adj_info.adj + tile.adj_info.near):
            tar_tile = self._get_tile_at_position(near_pos)
            tar_type = tar_tile.type
            if tar_type == TileType.FOREST and tar_tile.is_valid:
                matches += 1
        return MOUNTAIN_REWARD_PER_FOREST_NEARBY * matches

    def _get_score_helper_boats(self, tile: TileData):
        visited, queue = [], []
        visited.append(tile.pos)
        queue.append(tile.pos)
        while queue:
            next_pos = queue.pop(0)
            next_tile = self._get_tile_at_position(next_pos)
            if next_tile.is_valid:
                if next_tile.type in ON_ISLAND_TILE_TYPES or next_tile.on_island:
                    return abs(next_pos.col - tile.pos.col) + abs(next_pos.row - tile.pos.row)
                for neighbor in next_tile.adj_info.adj:
                    if neighbor not in visited:
                        visited.append(neighbor)
                        queue.append(neighbor)
        return max(self.row_num, self.col_num)

    def _get_score_helper_waves(self, tile: TileData):
        for cr_pos in (tile.adj_info.col + tile.adj_info.row):
            tar_tile = self._get_tile_at_position(cr_pos)
            tar_type = tar_tile.type
            if tar_type == TileType.WAVES and tar_tile.is_valid:
                return 0
        return WAVES_REWARD_IF_UNIQUE_COLUMN_ROW

    def _strict_revalidation_of_all_tiles(self):
        for tile_pos in self.tile_map.keys():
            tile = self._get_tile_at_position(tile_pos)
            tile.validate_tile_type()

    def add_tile_type_at_position(self, tile_type: TileType, pos: Position):
        tile = self._get_tile_at_position(pos)
        if tile.is_occupied:
            raise ValueError("Tile Has Been Occupied")
        tile.add_type(tile_type)

    def get_score(self, is_lenient: bool = True):
        if not is_lenient:
            self._strict_revalidation_of_all_tiles()
        score = 0
        for tile_pos in self.tile_map.keys():
            score += self._get_score_at_position(tile_pos)
        return score

    def add_island(self, lo_island_pos: List[Position]):
        lo_known_shore_pos = []
        lo_valid_island_tiles = []
        for pos in lo_island_pos:
            tile = self._get_tile_at_position(pos)
            if tile in lo_valid_island_tiles:
                raise ValueError("Assigned Island Contains Duplicate Tile Positions")
            if tile.on_island:
                raise ValueError("Assigned Island Overlapping with Some Previous Island")
            is_isolated = True
            for shore_candidate_pos in tile.adj_info.adj:
                if shore_candidate_pos not in lo_island_pos and shore_candidate_pos not in lo_known_shore_pos:
                    if self._get_tile_at_position(shore_candidate_pos).on_island:
                        raise ValueError("Assigned Island Overlapping with Previous Island")
                    lo_known_shore_pos.append(shore_candidate_pos)
                elif shore_candidate_pos in lo_island_pos and is_isolated:
                    is_isolated = False
            if is_isolated:
                raise ValueError("Assigned Island is Not Connected")
            lo_valid_island_tiles.append(tile)
        for tile in lo_valid_island_tiles:
            tile.mark_as_island()
        for pos in lo_known_shore_pos:
            self._get_tile_at_position(pos).mark_as_shore()
        self.islands.append(lo_island_pos)

    def view_board_cli(self):
        for r in range(self.row_num):
            row_str = ""
            for c in range(self.col_num):
                row_str += "   " + str(self._get_tile_at_position(Position(c, r)).type.value)
            print(row_str + "\n")

    def get_tile_array(self) -> list[list[int]]:
        lo_rows = []
        for r in range(self.row_num):
            row = []
            for c in range(self.col_num):
                row.append(self._get_tile_at_position(Position(c, r)).type.value)
            lo_rows.append(row)
        return lo_rows
