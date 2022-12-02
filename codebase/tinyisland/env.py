from gym import Env
from gym.spaces import Box, Discrete


class CustomEnv(Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self, arg1, arg2, ...):
    super(CustomEnv, self).__init__()
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)

  def step(self, action):
    # Execute one time step within the environment
    ...

  def render(self, mode='human', close=False):
    # Render the environment to the screen
    ...

  def reset(self):
    # Reset the state of the environment to an initial state
    ...
