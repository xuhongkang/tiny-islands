from typing import List, Tuple
from codebase.minisland.model import GameState
import copy
import time


def bfs_high_score(col_num: int, row_num: int, turn_limit: int,
                   choice_num: int, seed_int: int) -> Tuple[int, List[int]]:
    init_state = GameState(col_num, row_num, turn_limit, choice_num, seed_int)
    memo = dict()
    memo[init_state] = []
    for i in range(turn_limit):
        lo_new_states = dict()
        for state_on_turn in memo:
            path = memo[state_on_turn]
            for n in range(choice_num):
                state_n = copy.deepcopy(state_on_turn)
                state_n.choose_option(n)
                path_n = path.copy()
                path_n.append(n)
                lo_new_states[state_n] = path_n
        memo = lo_new_states
    max_score = 0
    for state_on_turn in memo:
        if state_on_turn.score > max_score:
            max_score = state_on_turn.score
    for state_on_turn in memo:
        if state_on_turn.score == max_score:
            return max_score, memo[state_on_turn]
    return max_score, []


def bfs_high_score_with_pruning(col_num: int, row_num: int, turn_limit: int,
                                choice_num: int, seed_int: int) -> Tuple[int, List[int]]:
    init_state = GameState(col_num, row_num, turn_limit, choice_num, seed_int)
    memo = dict()
    memo[init_state] = []
    for i in range(turn_limit):
        lo_new_states = dict()
        for state_on_turn in memo:
            state_score = state_on_turn.score
            path = memo[state_on_turn]
            for n in range(choice_num):
                state_n = copy.deepcopy(state_on_turn)
                state_n.choose_option(n)
                if state_n.score < 0 or state_n.score < state_score:
                    continue
                path_n = path.copy()
                path_n.append(n)
                lo_new_states[state_n] = path_n
        memo = lo_new_states
    max_score = 0
    for state_on_turn in memo:
        if state_on_turn.score > max_score:
            max_score = state_on_turn.score
    for state_on_turn in memo:
        if state_on_turn.score == max_score:
            return max_score, memo[state_on_turn]
    return max_score, []


if __name__ == "__main__":
    print("-------------------------------------------------")
    start_time = time.time()
    print("Running BFS HighScore")
    high_score, optimal_path = bfs_high_score(5, 5, 10, 2, 0)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Computed High Score is: " + str(high_score))
    print("Computed Optimal Path:")
    print(optimal_path)
    print("-------------------------------------------------")
    start_time = time.time()
    print("Running BFS HighScore With Pruning")
    high_score, optimal_path = bfs_high_score_with_pruning(5, 5, 10, 2, 0)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Computed High Score is: " + str(high_score))
    print("Computed Optimal Path:")
    print(optimal_path)
    print("-------------------------------------------------")
    print("Running Simulation Using Optimal Path...")
    state = GameState(5, 5, 10, 2, 0)
    for choice in optimal_path:
        state.choose_option(choice)
    print("Simulated High Score is: " + str(state.score))
    print("-------------------------------------------------")
