# board.py - Board
### Description:
A Board is a representation of the 9x9 grid of tiles in Tiny Islands, 
it supports the following pieces of functionality.

1. Holding data on a grid of tiles of fixed dimensions
   (Meaning its tiles only need to be initialized once)
2. Support the mutation of tile data (Quick retrieval of tiles given position)
3. Support quick lookup of a tile's
   "touching" (adjacent) tiles and "nearby" (surrounding) tiles
4. Support marking a limited valid path (tree) of the grid of tiles as "Islands"
5. Retrieve a list of tiles given the target type (cluster, row, column)

Helper Methods Needed:
1. Retrieving a given tile's data based on given position
2. Validating whether a supplied position is in bounds
3. Validating whether a tile is occupied