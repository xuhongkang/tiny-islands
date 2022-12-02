from typing import List, Tuple, Dict
from codebase.minisland.model import GameState
import copy
import time


def bfs_high_score(init_state: GameState) -> Tuple[int, List[int]]:
    memo = dict()
    memo[init_state] = []
    for i in range(init_state.turn_limit):
        lo_new_states = dict()
        for state_on_turn in memo:
            path = memo[state_on_turn]
            for n in range(init_state.choice_count):
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


def bfs_high_score_with_pruning(init_state: GameState) -> Tuple[int, List[int]]:
    memo = dict()
    memo[init_state] = []
    for i in range(init_state.turn_limit):
        lo_new_states = dict()
        for state_on_turn in memo:
            state_score = state_on_turn.score
            path = memo[state_on_turn]
            for n in range(init_state.choice_count):
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


# Depth Limited BFS search which prunes a percentage of the nodes after maxing the depth counter
def depth_limited_bfs_high_score(init_state: GameState, depth: int, pct_to_prune: float) -> Tuple[int, List[int]]:
    memo = dict()
    memo[init_state] = []
    counter = 0
    for i in range(init_state.turn_limit):
        lo_new_states = dict()
        for state_on_turn in memo:
            state_score = state_on_turn.score
            path = memo[state_on_turn]
            for n in range(init_state.choice_count):
                state_n = copy.deepcopy(state_on_turn)
                state_n.choose_option(n)
                if state_n.score < 0 or state_n.score < state_score:
                    continue
                path_n = path.copy()
                path_n.append(n)
                lo_new_states[state_n] = path_n
        memo = lo_new_states
        if counter == depth:
            prune_percentage(memo, pct_to_prune)
            counter = 0
        else:
            counter += 1
    max_score = 0
    for state_on_turn in memo:
        if state_on_turn.score > max_score:
            max_score = state_on_turn.score
    for state_on_turn in memo:
        if state_on_turn.score == max_score:
            return max_score, memo[state_on_turn]
    return max_score, []


def prune_percentage(memo: Dict[GameState, List[int]], pct: float):
    memo_length = len(memo)
    states = sorted(list(memo.keys()), key=lambda key: key.score, reverse=True)
    for i in range(int(memo_length * pct)):
        memo.pop(states.pop())


if __name__ == "__main__":
    config_state = GameState(6, 6, 12, 2, 0)
    print("-------------------------------------------------")
    start_time = time.time()
    print("Running BFS HighScore")
    high_score, optimal_path = bfs_high_score(config_state)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Computed High Score is: " + str(high_score))
    print("Computed Optimal Path:")
    print(optimal_path)
    print("-------------------------------------------------")
    start_time = time.time()
    print("Running BFS HighScore With Pruning")
    high_score, optimal_path = bfs_high_score_with_pruning(config_state)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Computed High Score is: " + str(high_score))
    print("Computed Optimal Path:")
    print(optimal_path)
    print("-------------------------------------------------")
    start_time = time.time()
    print("Running Depth Limited BFS HighScore With Pruning")
    high_score, optimal_path = depth_limited_bfs_high_score(config_state, 5, 0.2)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Computed High Score is: " + str(high_score))
    print("Computed Optimal Path:")
    print(optimal_path)
    print("-------------------------------------------------")
    print("Running Simulation Using Optimal Path...")
    state = config_state
    for choice in optimal_path:
        state.choose_option(choice)
    print("Simulated High Score is: " + str(state.score))
    print("-------------------------------------------------")
