from typing import Callable, List, Tuple
from enum import Enum


class SearchRange(Enum):
    """
    Represents a location based relationship a tile can have with another tile.
    """
    ADJ = "adjacent"
    NEAR = "near"
    COLUMN = "column"
    ROW = "row"


class ScoringLogic:
    def __init__(self, type_name_match_logic: Callable[[str], bool], unit_score: int, base_score: int,
                 search_range: List[SearchRange], only_once: bool = False):
        self.match_logic = type_name_match_logic
        self.unit_score = unit_score
        self.base_score = base_score
        self.search_range = search_range
        self.is_repeat = not only_once

    def get_score(self, adj: List[str], near: List[str], col: List[str], row: List[str]) -> int:
        """
        Groups candidate tiles by the searchRange type.
        Scores based on the quantity of candidate tile name and their searchRange type.
        :param adj: List of candidates adjacent.
        :param near: List of candidates near.
        :param col: list of candidates in the same column.
        :param row: List of candidates in the same row.
        :return: Returns the scoring of a single compared to all other candidates.
        """
        target_names, counter = [], 0
        if SearchRange.NEAR in self.search_range:
            target_names.extend(adj)
            target_names.extend(near)
        elif SearchRange.ADJ in self.search_range:
            target_names.extend(adj)
        if SearchRange.COLUMN in self.search_range:
            target_names.extend(col)
        if SearchRange.ROW in self.search_range:
            target_names.extend(row)

        for type_name in target_names:
            if self.match_logic(type_name):
                if self.is_repeat:
                    counter += 1
                else:
                    return self.unit_score
        return self.base_score + counter * self.unit_score

"""
The representation of a Tile type contains a String name and a List with logic for scoring the type. 
"""
class TileType:
    def __init__(self, name: str, logic: List[ScoringLogic]):
        self.name = name
        self.logic = logic

    def get_score(self, adj: List[str], near: List[str], col: List[str], row: List[str]) -> int:

        score = 0
        for rule in self.logic:
            score += rule.get_score(adj, near, col, row)
        return score

"""
Currently Three types of Tile + an Empty.
"""
class KnownTypeTypes(Enum):
    EMPTY = TileType("E", [])
    TypeA = TileType("A",
                     [ScoringLogic((lambda name: name == 'A'), -2, 2, [SearchRange.COLUMN, SearchRange.ROW], True)])
    TypeB = TileType("B", [ScoringLogic((lambda name: name == 'B'), 1, 0, [SearchRange.NEAR], False)])
    TypeC = TileType("C", [ScoringLogic((lambda name: name == 'C'), -2, 0, [SearchRange.ADJ], False),
                           ScoringLogic((lambda name: name == "A" or name == "B"), 1, 0, [SearchRange.NEAR], False)])


"""
A tile contains position, and a tuple of two list of ints representing touching tiles and nearby tiles.
"""
class TileData:
    def __init__(self, pos_x: int, pos_y: int, adj_info: Tuple[List[Tuple[int, int]], List[Tuple[int, int]],
                                                               List[Tuple[int, int]], List[Tuple[int, int]]]):
        self.type = KnownTypeTypes.EMPTY
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_occupied = False
        self.adj_info = adj_info

    def add_type(self, tar: KnownTypeTypes):
        """
        Setter method for a tile data.
        :param tar: Enum of Tile types. Throws an exception if type EMPTY
        """
        if tar == KnownTypeTypes.EMPTY:
            raise Exception("Placing Empty TileData Type")
        self.type = tar
        self.is_occupied = True

    def get_score(self, positions_to_tiles: Callable[[Tuple[List[Tuple[int, int]], List[Tuple[int, int]],
                                                            List[Tuple[int, int]], List[Tuple[int, int]]]],
                                                     Tuple[List[str], ...]]) -> int:
        if not isinstance(self.type.value, TileType):
            raise Exception("TileData type not a TileType")
        adj, near, col, row = positions_to_tiles(self.adj_info)
        return self.type.value.get_score(adj, near, col, row)


class Board:
    def __init__(self, col_num: int, row_num: int):
        self.col_num = col_num
        self.row_num = row_num
        self.tile_map = dict()
        for r in range(row_num):
            for c in range(col_num):
                adj_info = self._generate_adjacency_info((c, r))
                self.tile_map[(c, r)] = TileData(c, r, adj_info)

    def _generate_adjacency_info(self, pos: Tuple[int, int]) -> (Tuple[List[Tuple[int, int]], List[Tuple[int, int]],
                                                                       List[Tuple[int, int]], List[Tuple[int, int]]]):
        """
        Helper Method for generating valid adjacency info.
        :param pos: A tuple of two ints representing the position from which to generate adjacency info.
        :return: A tuple of two list of ints representing touching tiles and nearby tiles.
        """
        pos_x, pos_y = pos
        adj, near, col, row = list(), list(), list(), list()
        if pos_x < 8:
            adj.append((pos_x + 1, pos_y))
        if pos_x > 0:
            adj.append((pos_x - 1, pos_y))
        if pos_y < 8:
            adj.append((pos_x, pos_y - 1))
        if pos_y > 0:
            adj.append((pos_x, pos_y + 1))
        if pos_x < 8 and pos_y < 8:
            near.append((pos_x + 1, pos_y + 1))
        if pos_x < 8 and pos_y > 0:
            near.append((pos_x + 1, pos_y - 1))
        if pos_x > 0 and pos_y < 8:
            near.append((pos_x - 1, pos_y + 1))
        if pos_x > 0 and pos_y > 0:
            near.append((pos_x - 1, pos_y - 1))
        for r in range(self.row_num):
            if r != pos_y:
                col.append((pos_x, r))
        for c in range(self.col_num):
            if c != pos_x:
                row.append((pos_y, c))
        return adj, near, col, row


    def _get_tile_at_position(self, pos: Tuple[int, int]) -> TileData:
        """
        Helper getter method for single tile data.
        :param pos: A tuple of two ints representing the position (COORDINATES).
        :return: TileData at the coordinate. Throws an Exception if the coordinate is outside the board.
        """
        x, y = pos
        if x < 0 or y < 0 or x >= self.col_num or y >= self.row_num:
            raise Exception("Position Outside Board Dimensions")
        return self.tile_map[pos]

    def _get_tiles_at_positions(self, lo_pos: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        :param lo_pos: A list of tuples of two ints representing the position (COORDINATES).
        :return: A list of TileData
        """
        lo_tiles = list()
        for pos in lo_pos:
            lo_tiles.append(self._get_tile_at_position(pos))
        return lo_tiles

    def _get_type_names_for_adjacency_info(self, adj_info: Tuple[List[Tuple[int, int]], List[Tuple[int, int]],
                                                                 List[Tuple[int, int]], List[Tuple[int, int]]]) -> \
            Tuple[List[str], ...]:
        lo_type_adj_info = list()
        for lo_pos in adj_info:
            lo_types, lo_tiles = list(), self._get_tiles_at_positions(lo_pos)
            for tile in lo_tiles:
                lo_types.append(str(tile.type.value.name))
            lo_type_adj_info.append(lo_types)
        return tuple(lo_type_adj_info)

    def get_vacant_tile_positions(self):
        vacant_tiles = list()
        for tile_pos in self.tile_map.keys():
            tile = self._get_tile_at_position(tile_pos)
            if not tile.is_occupied:
                vacant_tiles.append(tile_pos)
        return vacant_tiles

    def add_tile_type(self, pos: Tuple[int, int], tile_type: KnownTypeTypes):
        self._get_tile_at_position(pos).add_type(tile_type)

    def get_score(self):
        score = 0
        for tile_pos in self.tile_map.keys():
            tile = self._get_tile_at_position(tile_pos)
            if tile.is_occupied:
                score += tile.get_score(self._get_type_names_for_adjacency_info)
        return score

    def view_cli(self):
        for r in range(self.row_num):
            row_str = ""
            for c in range(self.col_num):
                row_str += " " + self._get_tile_at_position((c, r)).type.value.name
            print(row_str + "\n")


if __name__ == "__main__":
    board = Board(5, 5)
    board.add_tile_type((2, 1), KnownTypeTypes.TypeA)
    board.view_cli()
    print("Score: " + str(board.get_score()) + "\n")
    board.add_tile_type((2, 2), KnownTypeTypes.TypeB)
    board.view_cli()
    print("Score: " + str(board.get_score()) + "\n")
    board.add_tile_type((2, 3), KnownTypeTypes.TypeC)
    board.view_cli()
    print("Score: " + str(board.get_score()) + "\n")
