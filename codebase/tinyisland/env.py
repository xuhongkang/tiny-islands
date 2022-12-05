from typing import Optional

from gym import Env
import random as rand

from gym.core import ActType
from gym.spaces import Dict, Tuple, Box, Discrete

from codebase.tinyisland.Board import Board
from codebase.tinyisland.Tile import TileType, Position


def _compute_all_choices_based_on_seed(seed_num: Optional[int] = None):
    all_choices = []
    if seed_num is not None:
        rand.seed(seed_num)
    else:
        rand.seed(rand.randint)
    for i in range(27):
        choices = dict()
        choice0 = dict()
        cluster0 = rand.randrange(3)
        cluster_num0 = rand.randrange(9)
        choice0["tile_type"] = rand.randrange(len(TileType))
        if cluster0 == 0:
            if cluster_num0 == 0:
                choice0["target_positions"] = (
                    Position(0, 0), Position(0, 1), Position(0, 2), Position(0, 3), Position(0, 4), Position(0, 5),
                    Position(0, 6), Position(0, 7), Position(0, 8))
            elif cluster_num0 == 1:
                choice0["target_positions"] = (
                    Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3), Position(1, 4), Position(1, 5),
                    Position(1, 6), Position(1, 7), Position(1, 8))
            elif cluster_num0 == 2:
                choice0["target_positions"] = (
                    Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3), Position(2, 4), Position(2, 5),
                    Position(2, 6), Position(2, 7), Position(2, 8))
            elif cluster_num0 == 3:
                choice0["target_positions"] = (
                    Position(3, 0), Position(3, 1), Position(3, 2), Position(3, 3), Position(3, 4), Position(3, 5),
                    Position(3, 6), Position(3, 7), Position(3, 8))
            elif cluster_num0 == 4:
                choice0["target_positions"] = (
                    Position(4, 0), Position(4, 1), Position(4, 2), Position(4, 3), Position(4, 4), Position(4, 5),
                    Position(4, 6), Position(4, 7), Position(4, 8))
            elif cluster_num0 == 5:
                choice0["target_positions"] = (
                    Position(5, 0), Position(5, 1), Position(5, 2), Position(5, 3), Position(5, 4), Position(5, 5),
                    Position(5, 6), Position(5, 7), Position(5, 8))
            elif cluster_num0 == 6:
                choice0["target_positions"] = (
                    Position(6, 0), Position(6, 1), Position(6, 2), Position(6, 3), Position(6, 4), Position(6, 5),
                    Position(6, 6), Position(6, 7), Position(6, 8))
            elif cluster_num0 == 7:
                choice0["target_positions"] = (
                    Position(7, 0), Position(7, 1), Position(7, 2), Position(7, 3), Position(7, 4), Position(7, 5),
                    Position(7, 6), Position(7, 7), Position(7, 8))
            elif cluster_num0 == 8:
                choice0["target_positions"] = (
                    Position(8, 0), Position(8, 1), Position(8, 2), Position(8, 3), Position(8, 4), Position(8, 5),
                    Position(8, 6), Position(8, 7), Position(8, 8))
        elif cluster0 == 1:
            if cluster_num0 == 0:
                choice0["target_positions"] = (
                    Position(0, 0), Position(1, 0), Position(2, 0), Position(3, 0), Position(4, 0), Position(5, 0),
                    Position(6, 0), Position(7, 0), Position(8, 0))
            elif cluster_num0 == 1:
                choice0["target_positions"] = (
                    Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1), Position(4, 1), Position(5, 1),
                    Position(6, 1), Position(7, 1), Position(8, 1))
            elif cluster_num0 == 2:
                choice0["target_positions"] = (
                    Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2), Position(4, 2), Position(5, 2),
                    Position(6, 2), Position(7, 2), Position(8, 2))
            elif cluster_num0 == 3:
                choice0["target_positions"] = (
                    Position(0, 3), Position(1, 3), Position(2, 3), Position(3, 3), Position(4, 3), Position(5, 3),
                    Position(6, 3), Position(7, 3), Position(8, 3))
            elif cluster_num0 == 4:
                choice0["target_positions"] = (
                    Position(0, 4), Position(1, 4), Position(2, 4), Position(3, 4), Position(4, 4), Position(5, 4),
                    Position(6, 4), Position(7, 4), Position(8, 4))
            elif cluster_num0 == 5:
                choice0["target_positions"] = (
                    Position(0, 5), Position(1, 5), Position(2, 5), Position(3, 5), Position(4, 5), Position(5, 5),
                    Position(6, 5), Position(7, 5), Position(8, 5))
            elif cluster_num0 == 6:
                choice0["target_positions"] = (
                    Position(0, 6), Position(1, 6), Position(2, 6), Position(3, 6), Position(4, 6), Position(5, 6),
                    Position(6, 6), Position(7, 6), Position(8, 6))
            elif cluster_num0 == 7:
                choice0["target_positions"] = (
                    Position(0, 7), Position(1, 7), Position(2, 7), Position(3, 7), Position(4, 7), Position(5, 7),
                    Position(6, 7), Position(7, 7), Position(8, 7))
            elif cluster_num0 == 8:
                choice0["target_positions"] = (
                    Position(0, 8), Position(1, 8), Position(2, 8), Position(3, 8), Position(4, 8), Position(5, 8),
                    Position(6, 8), Position(7, 8), Position(8, 8))
        elif cluster0 == 2:
            if cluster_num0 == 0:
                choice0["target_positions"] = (
                    Position(0, 0), Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2),
                    Position(2, 0), Position(2, 1), Position(2, 2))
            elif cluster_num0 == 1:
                choice0["target_positions"] = (
                    Position(0, 3), Position(0, 4), Position(0, 5), Position(1, 3), Position(1, 4), Position(1, 5),
                    Position(2, 3), Position(2, 4), Position(2, 5))
            elif cluster_num0 == 2:
                choice0["target_positions"] = (
                    Position(0, 6), Position(0, 7), Position(0, 8), Position(1, 6), Position(1, 7), Position(1, 8),
                    Position(2, 6), Position(2, 7), Position(2, 8))
            elif cluster_num0 == 3:
                choice0["target_positions"] = (
                    Position(3, 0), Position(3, 1), Position(3, 2), Position(4, 0), Position(4, 1), Position(4, 2),
                    Position(5, 0), Position(5, 1), Position(5, 2))
            elif cluster_num0 == 4:
                choice0["target_positions"] = (
                    Position(3, 3), Position(3, 4), Position(3, 5), Position(4, 3), Position(4, 4), Position(4, 5),
                    Position(5, 3), Position(5, 4), Position(5, 5))
            elif cluster_num0 == 5:
                choice0["target_positions"] = (
                    Position(3, 6), Position(3, 7), Position(3, 8), Position(4, 6), Position(4, 7), Position(4, 8),
                    Position(5, 6), Position(5, 7), Position(5, 8))
            elif cluster_num0 == 6:
                choice0["target_positions"] = (
                    Position(6, 0), Position(6, 1), Position(6, 2), Position(7, 0), Position(7, 1), Position(7, 2),
                    Position(8, 0), Position(8, 1), Position(8, 2))
            elif cluster_num0 == 7:
                choice0["target_positions"] = (
                    Position(6, 3), Position(6, 4), Position(6, 5), Position(7, 3), Position(7, 4), Position(7, 5),
                    Position(7, 3), Position(7, 4), Position(7, 5))
            elif cluster_num0 == 8:
                choice0["target_positions"] = (
                    Position(6, 6), Position(6, 7), Position(6, 8), Position(7, 6), Position(7, 7), Position(7, 8),
                    Position(8, 6), Position(8, 7), Position(8, 8))
        choices["choice0"] = choice0
        choice1 = dict()
        cluster1 = rand.randrange(3)
        cluster_num1 = rand.randrange(9)
        choice1["tile_type"] = rand.randrange(len(TileType))
        if cluster1 == 0:
            if cluster_num1 == 0:
                choice1["target_positions"] = (
                    Position(0, 0), Position(0, 1), Position(0, 2), Position(0, 3), Position(0, 4), Position(0, 5),
                    Position(0, 6), Position(0, 7), Position(0, 8))
            elif cluster_num1 == 1:
                choice1["target_positions"] = (
                    Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3), Position(1, 4), Position(1, 5),
                    Position(1, 6), Position(1, 7), Position(1, 8))
            elif cluster_num1 == 2:
                choice1["target_positions"] = (
                    Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3), Position(2, 4), Position(2, 5),
                    Position(2, 6), Position(2, 7), Position(2, 8))
            elif cluster_num1 == 3:
                choice1["target_positions"] = (
                    Position(3, 0), Position(3, 1), Position(3, 2), Position(3, 3), Position(3, 4), Position(3, 5),
                    Position(3, 6), Position(3, 7), Position(3, 8))
            elif cluster_num1 == 4:
                choice1["target_positions"] = (
                    Position(4, 0), Position(4, 1), Position(4, 2), Position(4, 3), Position(4, 4), Position(4, 5),
                    Position(4, 6), Position(4, 7), Position(4, 8))
            elif cluster_num1 == 5:
                choice1["target_positions"] = (
                    Position(5, 0), Position(5, 1), Position(5, 2), Position(5, 3), Position(5, 4), Position(5, 5),
                    Position(5, 6), Position(5, 7), Position(5, 8))
            elif cluster_num1 == 6:
                choice1["target_positions"] = (
                    Position(6, 0), Position(6, 1), Position(6, 2), Position(6, 3), Position(6, 4), Position(6, 5),
                    Position(6, 6), Position(6, 7), Position(6, 8))
            elif cluster_num1 == 7:
                choice1["target_positions"] = (
                    Position(7, 0), Position(7, 1), Position(7, 2), Position(7, 3), Position(7, 4), Position(7, 5),
                    Position(7, 6), Position(7, 7), Position(7, 8))
            elif cluster_num1 == 8:
                choice1["target_positions"] = (
                    Position(8, 0), Position(8, 1), Position(8, 2), Position(8, 3), Position(8, 4), Position(8, 5),
                    Position(8, 6), Position(8, 7), Position(8, 8))
        elif cluster1 == 1:
            if cluster_num1 == 0:
                choice1["target_positions"] = (
                    Position(0, 0), Position(1, 0), Position(2, 0), Position(3, 0), Position(4, 0), Position(5, 0),
                    Position(6, 0), Position(7, 0), Position(8, 0))
            elif cluster_num1 == 1:
                choice1["target_positions"] = (
                    Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1), Position(4, 1), Position(5, 1),
                    Position(6, 1), Position(7, 1), Position(8, 1))
            elif cluster_num1 == 2:
                choice1["target_positions"] = (
                    Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2), Position(4, 2), Position(5, 2),
                    Position(6, 2), Position(7, 2), Position(8, 2))
            elif cluster_num1 == 3:
                choice1["target_positions"] = (
                    Position(0, 3), Position(1, 3), Position(2, 3), Position(3, 3), Position(4, 3), Position(5, 3),
                    Position(6, 3), Position(7, 3), Position(8, 3))
            elif cluster_num1 == 4:
                choice1["target_positions"] = (
                    Position(0, 4), Position(1, 4), Position(2, 4), Position(3, 4), Position(4, 4), Position(5, 4),
                    Position(6, 4), Position(7, 4), Position(8, 4))
            elif cluster_num1 == 5:
                choice1["target_positions"] = (
                    Position(0, 5), Position(1, 5), Position(2, 5), Position(3, 5), Position(4, 5), Position(5, 5),
                    Position(6, 5), Position(7, 5), Position(8, 5))
            elif cluster_num1 == 6:
                choice1["target_positions"] = (
                    Position(0, 6), Position(1, 6), Position(2, 6), Position(3, 6), Position(4, 6), Position(5, 6),
                    Position(6, 6), Position(7, 6), Position(8, 6))
            elif cluster_num1 == 7:
                choice1["target_positions"] = (
                    Position(0, 7), Position(1, 7), Position(2, 7), Position(3, 7), Position(4, 7), Position(5, 7),
                    Position(6, 7), Position(7, 7), Position(8, 7))
            elif cluster_num1 == 8:
                choice1["target_positions"] = (
                    Position(0, 8), Position(1, 8), Position(2, 8), Position(3, 8), Position(4, 8), Position(5, 8),
                    Position(6, 8), Position(7, 8), Position(8, 8))
        elif cluster1 == 2:
            if cluster_num1 == 0:
                choice1["target_positions"] = (
                    Position(0, 0), Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2),
                    Position(2, 0), Position(2, 1), Position(2, 2))
            elif cluster_num1 == 1:
                choice1["target_positions"] = (
                    Position(0, 3), Position(0, 4), Position(0, 5), Position(1, 3), Position(1, 4), Position(1, 5),
                    Position(2, 3), Position(2, 4), Position(2, 5))
            elif cluster_num1 == 2:
                choice1["target_positions"] = (
                    Position(0, 6), Position(0, 7), Position(0, 8), Position(1, 6), Position(1, 7), Position(1, 8),
                    Position(2, 6), Position(2, 7), Position(2, 8))
            elif cluster_num1 == 3:
                choice1["target_positions"] = (
                    Position(3, 0), Position(3, 1), Position(3, 2), Position(4, 0), Position(4, 1), Position(4, 2),
                    Position(5, 0), Position(5, 1), Position(5, 2))
            elif cluster_num1 == 4:
                choice1["target_positions"] = (
                    Position(3, 3), Position(3, 4), Position(3, 5), Position(4, 3), Position(4, 4), Position(4, 5),
                    Position(5, 3), Position(5, 4), Position(5, 5))
            elif cluster_num1 == 5:
                choice1["target_positions"] = (
                    Position(3, 6), Position(3, 7), Position(3, 8), Position(4, 6), Position(4, 7), Position(4, 8),
                    Position(5, 6), Position(5, 7), Position(5, 8))
            elif cluster_num1 == 6:
                choice1["target_positions"] = (
                    Position(6, 0), Position(6, 1), Position(6, 2), Position(7, 0), Position(7, 1), Position(7, 2),
                    Position(8, 0), Position(8, 1), Position(8, 2))
            elif cluster_num1 == 7:
                choice1["target_positions"] = (
                    Position(6, 3), Position(6, 4), Position(6, 5), Position(7, 3), Position(7, 4), Position(7, 5),
                    Position(7, 3), Position(7, 4), Position(7, 5))
            elif cluster_num1 == 8:
                choice1["target_positions"] = (
                    Position(6, 6), Position(6, 7), Position(6, 8), Position(7, 6), Position(7, 7), Position(7, 8),
                    Position(8, 6), Position(8, 7), Position(8, 8))
        choices["choice1"] = 0
        all_choices.append(choices)
    return all_choices


class TinyIslandsWithoutIslands(Env):
    """Custom Environment that follows gym interface"""
    metadata = {"render.modes": ["human"
                                 # , "rgb_array"
                                 ], "render_fps": 4}

    def __init__(self, render_mode=None):
        self.window_size = 512
        self.action_space = Dict(
            {
                "choice": Discrete(2),
                "target_position:": Box(0, 8, shape=(2,), dtype=int)
            }
        )
        self.observation_space = Dict(
            {
                "board": Box(0, len(TileType) - 1, shape=(8, 8), dtype=Discrete),
                "score": int,
                "turns_passed": int,
                "choices": Dict(
                    {
                        "choice0": Dict(
                            {
                                "tile_type": Discrete(len(TileType)),
                                "target_positions": Tuple((Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int)))
                            }
                        ),
                        "choice1": Dict(
                            {
                                "tile_type": Discrete(len(TileType)),
                                "target_positions": Tuple((Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int),
                                                           Box(0, 8, shape=(2,), dtype=int)))
                            }
                        )
                    }
                )
            }
        )
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.reward_range = (-500, 100)
        self.window = None
        self.clock = None

    def step(self, action: ActType):
        done = False
        prev_reward = self.board.get_score()
        terminated = False
        choice_num = action["choice"]
        tar_position = action["target_position"]
        try:
            if choice_num == 0:
                choice = self.choices[self.turns_passed]["choice0"]
            elif choice_num == 1:
                choice = self.choices[self.turns_passed]["choice1"]
            else:
                raise ValueError("Wrong Input")
            if tar_position not in choice["target_positions"]:
                raise ValueError("Target Position Not in Choice")
            self.board.add_tile_type_at_position(TileType(choice["tile_type"]), tar_position)
            self.turns_passed += 1
            if self.turns_passed > 27:
                terminated = True
            reward = self.board.get_score() - prev_reward
        except ValueError:
            done = True
            reward = -500
        return self.board.get_tile_array(), terminated, reward, done, {}

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        self.board = Board()
        self.turns_passed = 0
        self.choices = _compute_all_choices_based_on_seed(seed)
        if self.render_mode == "human":
            self.render()
        initial_observation = dict()
        initial_observation["board"] = self.board.get_tile_array()
        initial_observation["score"] = 0
        initial_observation["turns_passed"] = 0
        initial_observation["choices"] = self.choices[0]
        return initial_observation, {}

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        ...
