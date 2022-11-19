# tile.py - Tile
A Tile is a data representation of one of the tile components of the board in Tiny Islands.
A Tile supports the following functionalities:

1. Holds information on its assigned position in the board on initialization
2. Holds information on its assigned terrain type (May only be assigned once after initialization)
3. Holds information on whether it's part of an island (May only be assigned once after initialization)
4. Mutates type given valid assignment, raises exception if not supported
5. Assign itself to be an island given valid assignment, raises exception if not supported