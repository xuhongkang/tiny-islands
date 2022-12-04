from enum import Enum

from tinyisland.Board import Board
import random as rand
from typing import List, Tuple

from tinyisland.Tile import TileType, Position


class BoardTileRange(Enum):
    COLUMN = 0
    ROW = 1
    CLUSTER = 2


class State:
    def __init__(self, seed_num: int = rand.randint):
        self.board = Board(9, 9)
        self.turns_passed = 0
        self.choices = self._compute_choices(seed_num)

    def _compute_choices(self, seed_num: int) -> List[Tuple[Tuple[TileType, BoardTileRange, int],
                                                            Tuple[TileType, BoardTileRange, int]]]:
        rand.seed(seed_num)
        lo_choices = []
        for i in range(28):
            tile_choice1 = TileType(rand.randrange(len(TileType) - 1) + 1)
            cluster_choice1 = BoardTileRange(rand.randrange(len(BoardTileRange) - 1) + 1)
            pos_idx1 = rand.randrange(9)
            tile_choice2 = TileType(rand.randrange(len(TileType) - 1) + 1)
            cluster_choice2 = BoardTileRange(rand.randrange(len(BoardTileRange) - 1) + 1)
            pos_idx2 = rand.randrange(9)
            lo_choices.append(((tile_choice1, cluster_choice1, pos_idx1), (tile_choice2, cluster_choice2, pos_idx2)))
        return lo_choices

    def get_choices(self) -> Tuple[Tuple[TileType, BoardTileRange, int], Tuple[TileType, BoardTileRange, int]]:
        return self.choices[self.turns_passed]

    def execute_turn(self, choice: int, tar_pos: Position):
        self.board.add_tile_type(self.get_choices()[choice][0], tar_pos)








if __name__ == "__main__":
    print("-------------------------------------------------")
    seed_int = rand.randrange(1000)
    state = GameState(3, 3, 4, 2, seed_int)
    print("Game Started! Seed: " + str(seed_int))
    print("-------------------------------------------------")
    while not state.has_game_ended():
        state.board.view_board_cli()
        state.view_choices_cli(state.get_choices())
        state.cli_get_move()
        print("-------------------------------------------------")
    print("You Won! Here's Your Final Island:\n")
    state.board.view_board_cli()
    print("Your Final Score is: " + str(state.score))
    print("-------------------------------------------------")