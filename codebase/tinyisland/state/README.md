# State.py
A State holds the board, the number of turns taken.
1. Take a move and attempt to mutate the game state (return copy?)
2. Evaluate current game state, return score.

Static method for generating random moves.


A move will either contain, Terrain, Pos,
or contain a path with restrictions on length/connectivity

A Choice will contain:
Two Random terrain_types: Terrain,
Tile_Group_Type: Enum, 
Tile_Group_Index: non-negative int less than 9