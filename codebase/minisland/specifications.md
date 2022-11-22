### Proposed New Tile Types and Associated Scoring Logic:

1. Type A

a. Gives +2 score if there’s not any other Type A sharing its row and column

2. Type B

a. Gives +1 score for each Type B near it

3. Type C

a. Gives +1 score for each Type A or Type B near it

b. Gives -2 score for each Type C adjacent to it

Explanation: After careful consideration, we believe that the above 3 types of tile design best
capture the many features of terrain tiles in Tiny Islands, and will be the candidates for the tiles
in our simplified model. This simplified model, whose mechanics will be introduced below, will
become the environment in which our agent will be trained for Milestone 2.

### Proposed New Rules and Mechanics:

1. The Board will consist of 25 (initially empty) Tiles ordered in a 5x5 grid.

2. A Tile is a unit located on the grid with a unique 2d Position. Tiles are initially empty,
but may be assigned specific Types. If a Tile has already been assigned a Type, it cannot
be reassigned. (This feature might conflict with MDP principles since the Seed will have
to offer alternative Choices if the tile at the initial target position has already been
assigned. This rule might be relaxed further in the future.)

3. Position is a unique identifier for Tiles denoting its 2D position on the Board. For a 5x5
Board, Positions may range from (0, 0) to (4, 4) where (x, y) represents the Tile in
column x on row y on the Board.

4. A Type is a specific typing for a Tile that represents a unique piece of scoring logic.
Scoring logic computes the individual score of a Tile, based on information about
adjacent (directly connected in at most 4 directions) or near (directly connected in at most4 directions) Tile to the reference Tile. Tiles with different Types score differently
individually.

5. At the start of the Turn, the agent chooses from a Choice. A Choice consists of two sets
of Tile Type-Position pairs. By selecting one of the sets, the state progresses to the next
state by changing the Type of the Tile at the paired Position to its target Type.

6. A Game of Tiny Mini Islands consists of 10 turns. The final score is calculated by adding
up all the individual scores of Tiles based on their Type.