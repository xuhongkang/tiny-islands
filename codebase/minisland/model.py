from typing import Callable, List, Tuple, Any
from enum import Enum
import random as Random


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


class TileType:
    """
    The representation of a Tile type contains a String name and a List with logic for scoring the type.
    """

    def __init__(self, name: str, logic: List[ScoringLogic]):
        self.name = name
        self.logic = logic

    def get_score(self, adj: List[str], near: List[str], col: List[str], row: List[str]) -> int:
        score = 0
        for rule in self.logic:
            score += rule.get_score(adj, near, col, row)
        return score


class KnownTileType(Enum):
    """
    Currently Three types of Tile + an Empty. Class open to change for adding new tile types.
    """
    EMPTY = TileType("E", [])
    TypeA = TileType("A",
                     [ScoringLogic((lambda name: name == 'A'), -2, 2, [SearchRange.COLUMN, SearchRange.ROW], True)])
    TypeB = TileType("B", [ScoringLogic((lambda name: name == 'B'), 1, 0, [SearchRange.NEAR], False)])
    TypeC = TileType("C", [ScoringLogic((lambda name: name == 'C'), -2, 0, [SearchRange.ADJ], False),
                           ScoringLogic((lambda name: name == "A" or name == "B"), 1, 0, [SearchRange.NEAR], False)])


class TileData:
    """
    A tile contains position, and a tuple of two list of ints representing touching tiles and nearby tiles.
    """

    def __init__(self, pos_x: int, pos_y: int, adj_info: Tuple[List[Tuple[int, int]], List[Tuple[int, int]],
                                                               List[Tuple[int, int]], List[Tuple[int, int]]]):
        self.type = KnownTileType.EMPTY
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_occupied = False
        self.adj_info = adj_info

    def add_type(self, tar: KnownTileType):
        """
        Setter method for a tile data.
        :param tar: Enum of Tile types. Throws an exception if type EMPTY
        """
        if tar == KnownTileType.EMPTY:
            raise ValueError("Placing Empty TileData Type")
        self.type = tar
        self.is_occupied = True

    def get_score(self, positions_to_tiles: Callable[[Tuple[List[Tuple[int, int]], List[Tuple[int, int]],
                                                            List[Tuple[int, int]], List[Tuple[int, int]]]],
                                                     Tuple[List[str], ...]]) -> int:
        if not isinstance(self.type.value, TileType):
            raise ValueError("TileData type not a TileType")
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
        if pos_x < self.col_num - 1:
            adj.append((pos_x + 1, pos_y))
        if pos_x > 0:
            adj.append((pos_x - 1, pos_y))
        if pos_y < self.row_num - 1:
            adj.append((pos_x, pos_y + 1))
        if pos_y > 0:
            adj.append((pos_x, pos_y - 1))
        if pos_x < self.col_num - 1 and pos_y < self.row_num - 1:
            near.append((pos_x + 1, pos_y + 1))
        if pos_x < self.col_num - 1 and pos_y > 0:
            near.append((pos_x + 1, pos_y - 1))
        if pos_x > 0 and pos_y < self.row_num - 1:
            near.append((pos_x - 1, pos_y + 1))
        if pos_x > 0 and pos_y > 0:
            near.append((pos_x - 1, pos_y - 1))
        for r in range(self.row_num - 1):
            if r != pos_y:
                col.append((pos_x, r))
        for c in range(self.col_num - 1):
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
            raise ValueError("Position Outside Board Dimensions")
        return self.tile_map[pos]

    def _get_tiles_at_positions(self, lo_pos: List[Tuple[int, int]]) -> List[TileData]:
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

    def add_tile_type(self, tile_type: KnownTileType, pos: Tuple[int, int]):
        tile = self._get_tile_at_position(pos)
        if tile.is_occupied:
            raise ValueError("Tile Has Been Occupied")
        tile.add_type(tile_type)

    def get_score(self):
        score = 0
        for tile_pos in self.tile_map.keys():
            tile = self._get_tile_at_position(tile_pos)
            if tile.is_occupied:
                score += tile.get_score(self._get_type_names_for_adjacency_info)
        return score

    def view_board_cli(self):
        for r in range(self.row_num):
            row_str = ""
            for c in range(self.col_num):
                row_str += " " + self._get_tile_at_position((c, r)).type.value.name
            print(row_str + "\n")


class GameState:
    def __init__(self, col_num: int, row_num: int, turn_limit: int, choice_count: int, seed_num: int):
        if col_num * row_num / choice_count < turn_limit:
            raise ValueError("More Turns than Tiles")
        self.col_num = col_num
        self.row_num = row_num
        self.board = Board(col_num, row_num)
        self.turns_passed = 0
        self.turn_limit = turn_limit
        self.choice_count = choice_count
        self.choices = self._compute_choices(seed_num)
        self.score = 0

    def _compute_choices(self, seed_num: int) -> List[Tuple[Tuple[Any, Tuple[int, int]], ...]]:
        Random.seed(seed_num)
        lo_choices, lo_types, known_pos = [], [], []
        for choice_type in KnownTileType:
            if choice_type != KnownTileType.EMPTY:
                lo_types.append(choice_type)
        for turn_num in range(self.turn_limit):
            choices, lo_pos = [], []
            last_choice = None
            for choice_num in range(self.choice_count):
                rand_type = lo_types[Random.randrange(len(lo_types))]
                rand_pos = (Random.randrange(self.col_num), Random.randrange(self.row_num))
                while last_choice == (rand_type, rand_pos) or rand_pos in known_pos:
                    rand_pos = (Random.randrange(self.col_num), Random.randrange(self.row_num))
                choice = (rand_type, rand_pos)
                lo_pos.append(rand_pos)
                choices.append(choice)
                last_choice = choice
            known_pos.extend(lo_pos)
            lo_choices.append(tuple(choices))
        return lo_choices

    def _execute_turn(self, choice_option: Tuple[Any, Tuple[int, int]]):
        self.board.add_tile_type(choice_option[0], choice_option[1])
        self.score = self.board.get_score()
        self.turns_passed += 1

    def get_choices(self) -> Tuple[Tuple[KnownTileType, Tuple[int, int]], ...]:
        return self.choices[self.turns_passed]

    def choose_option(self, option: int):
        if self.has_game_ended():
            raise ValueError("Game Finished")
        if option < 0 or option >= self.choice_count:
            raise ValueError("Invalid Option Given")
        turn_option = self.get_choices()[option]
        self._execute_turn(turn_option)

    def has_game_ended(self) -> bool:
        return self.turns_passed >= self.turn_limit

    def view_choices_cli(self, choices: Tuple[Tuple[KnownTileType, Tuple[int, int]], ...]):
        for choice_num in range(self.choice_count):
            option = choices[choice_num]
            print("Choice " + str(choice_num) + ":\n"
                                                "Position: (" + str(option[1][0]) + " " + str(option[1][1]) + ")\n"
                                                "TileType: " + option[0].value.name + "\n")

    def cli_get_move_helper(self):
        try:
            self.choose_option(int(input("Choose Your Option: ")))
        except ValueError as e:
            print(e)
            print("Please Try Again: ")
            self.cli_get_move_helper()


if __name__ == "__main__":
    seed = Random.randrange(1000)
    state = GameState(3, 3, 4, 2, seed)
    print("Game Started! Seed: " + str(seed))
    while not state.has_game_ended():
        state.board.view_board_cli()
        state.view_choices_cli(state.get_choices())
        state.cli_get_move_helper()
    print("You Won! Here's Your Final Island:\n")
    state.board.view_board_cli()
    print("Your Final Score is: " + str(state.score))
