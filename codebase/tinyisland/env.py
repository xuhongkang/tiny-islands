from gym import Env
from typing import Callable, List, Tuple, Any
from enum import Enum
import random as rand
from gym.spaces import Box, Discrete


class CustomEnv(Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(CustomEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        # Example for using image as input:

    def step(self, action):
        # Execute one time step within the environment
        ...

    def reset(self):
        # Reset the state of the environment to an initial state
        ...

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        ...








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
        rand.seed(seed_num)
        lo_choices, lo_types, known_pos = [], [], []
        for choice_type in KnownTileType:
            if choice_type != KnownTileType.EMPTY:
                lo_types.append(choice_type)
        for turn_num in range(self.turn_limit):
            choices, lo_pos = [], []
            last_choice = None
            for choice_num in range(self.choice_count):
                rand_type = lo_types[rand.randrange(len(lo_types))]
                rand_pos = (rand.randrange(self.col_num), rand.randrange(self.row_num))
                while last_choice == (rand_type, rand_pos) or rand_pos in known_pos:
                    rand_pos = (rand.randrange(self.col_num), rand.randrange(self.row_num))
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
                                                                                                              "TileType: " +
                  option[0].value.name + "\n")

    def cli_get_move(self):
        try:
            self.choose_option(int(input("Choose Your Option: ")))
        except ValueError as e:
            print(e)
            print("Please Try Again: ")
            self.cli_get_move()


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
