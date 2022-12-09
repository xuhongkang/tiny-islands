import math
from enum import Enum
from typing import Tuple, List
from tinyisland.Board import Board
import random as rand

from tinyisland.Tile import TileType, Position


class TileRange(Enum):
    COLUMN = "X"
    ROW = "Y"
    CLUSTER = "Z"


class Choice:
    def __init__(self, tile_type: TileType, tile_range: TileRange, range_idx: int):
        self.tile_type = tile_type
        self.tile_range = tile_range
        self.range_idx = range_idx

    def get_all_valid_positions(self, col_num: int = 9, row_num: int = 9):
        rlist = []
        if self.tile_range == TileRange.ROW:
            if self.range_idx >= row_num:
                raise ValueError("Invalid Row Index")
            else:
                for col_idx in range(col_num):
                    rlist.append(Position(col_idx, self.range_idx))
                return rlist
        elif self.tile_range == TileRange.COLUMN:
            if self.range_idx >= col_num:
                raise ValueError("Invalid Column Index")
            else:
                for row_idx in range(row_num):
                    rlist.append(Position(self.range_idx, row_idx))
                return rlist
        elif self.tile_range == TileRange.CLUSTER:
            if col_num != row_num:
                raise ValueError("Invalid Board Dimensions, Does not support Cluster")
            start_x = int(self.range_idx % col_num)
            start_y = int(self.range_idx / row_num)
            for y in range(col_num):
                for x in range(col_num):
                    rlist.append(Position(start_x + x, start_y + y))
            return rlist



class State:
    def __init__(self, seed_num: int = rand.randint, col_num: int = 9, row_num: int = 9,
                 choice_num: int = 2, turn_limit: int = 30):
        self.board = Board(col_num, row_num)
        self.turn_limit = turn_limit
        self.turns_passed = 0
        self.choice_num = choice_num
        self.choices = self.compute_all_choices(seed_num)

    def compute_all_choices(self, seed_num: int) -> List[List[Choice]]:
        rand.seed(seed_num)
        choices_in_game = []
        for turn_num in range(self.turn_limit):
            choices_in_turn = []
            for choice_idx in range(self.choice_num):
                r_type = list(TileType)[rand.randrange(len(TileType))]

                choices_in_turn.append(Choice())
