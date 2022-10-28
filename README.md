# Tiny Islands AI Project
AI Project for an itch.io indie board game Tiny Islands (2019)

[Tiny Islands](https://dr-d-king.itch.io/tiny-islands) is a turn-based grid-based strategy game that involves placing different terrain tiles and drawing islands to earn points. This project will involve two stages: The first is a state search algorithm to determine the best high score given a known seed; and the second would be to train a reinforcement learning model that can exceed at obtaining an effective high score without prior knowledge of the seed’s configurations.

## Team Members:
Alex Ma, Andrew Sayegh, Diego Valdivia Cox, Hongkang Xu

## Milestones:
1. Cost-opt search given a single state of board
2. Reinforced learning for any possible configuration state.


## Q: Describe the problem you are trying to address:

Make an optimal AI that completes the game with a high or even optimal score of the Game Tiny
Island.

## Q: What is the ideal outcome of the project? What do you expect to show?

### Stretch goals
- Make an optimal AI that completes a random game from start to finish with a high or even optimal score

### Minimum viable product
- Create a model of the game
- Given a seed, compute the optimal possible score using graph search to compute all goal
states.
- Create some sort of AI that can complete the game (may not be optimal solution)
- Utilizing the optimal possible score, train an agent using reinforcement learning to be
able to get close to that score without prior knowledge of the set of actions to choose
from.

## Q: What algorithms do you expect to use?
A* algorithm for traversing search graphs and generating goal states.
Custom Evaluation Function for pruning of “invalid” states where the score is penalized (there’s no coming back
A fine tuned hand written evaluation function for opening moves
Convolutional Neural Networks for optimizing ML models.
What topics / libraries / platforms, if any, will you
have to learn in order to undertake your project?
Numpy, Sci-learn, Tensorflow

## Q: Define milestones for your project:
### Milestone 1:
- Set up repo and project structure
- Object Oriented Approach to generating data representations of the Game Board and Tile

### Milestone 2:
- Experimental Function Search Agents
- Start with use of a* algorithm with evaluation function to traversing search graphs and
generating goal states to find optimal highscore.
- Due to the amount of possible goal states (without eval function) being somewhere
around 54^27, we might need to switch to probabilistic search with some degree of
pruning.

### Milestone 3:
- Applying possible reinforcement learning concepts to optimize path solving for randomized seeds (with n
knowledge of the environment)
