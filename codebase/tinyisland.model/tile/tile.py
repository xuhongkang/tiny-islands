from terrains import terrain as Terrain;


class Tile:
    def __init__(self, adj: list[tuple[int, int]], cor: list[tuple[int, int]]):
        """
        Constructor for Tile, given pos, sets pos, terrain to empty and is_on_tile to false.
        :param adj: A list of tile positions representing the directly adjacent positions.
        :param cor: A list of tile positions representing the nearby "corner" positions.
        """
        self.adj = adj
        self.cor = cor
        self.terrain_type = Terrain.EMPTY
        self.is_on_island = False

    def _has_set_terrain(self) -> bool:
        """
        Private Method for checking if the terrain of the tile has been set to a non-EMPTY value.
        :return: True if it has been set, False if otherwise.
        """
        return self.terrain_type != Terrain.EMPTY

    def get_terrain(self) -> Terrain:
        """
        Public method for getting the terrain type of the tile.
        :return: A terrain containing terrain information about the tile.
        """
        return self.terrain_type

    def is_terrain(self, terrain: Terrain) -> bool:
        """
        Checks if the terrain is the given terrain.
        :param terrain: A Terrain representing the terrain with which to compare.
        :return: True if the tile has the given terrain, False if otherwise.
        """
        return self.terrain_type == terrain

    def set_terrain(self, terrain: Terrain):
        """
        Public method for setting the terrain type of the tile.
        :param terrain: A Terrain to which attempts to assign the terrain of the tile.
        :exception: Raises exception if the terrain has been set.
        """
        if self._has_set_terrain():
            raise Exception("Terrain Already Assigned.")
        self.terrain_type = terrain

    def is_on_island(self) -> bool:
        """
        Public method for checking if the tile is an island.
        :return: True if the tile is on an island, False if otherwise.
        """
        return self.is_on_island

    def toggle_on_island(self):
        """
        Public method for toggling the tile to be on or off an island.
        """
        self.is_on_island = not self.is_on_island

    def get_touching(self) -> list[tuple[int, int]]:
        """
        Gets all the positions of touching (adjacent) tiles.
        :return: A List of tuples of two ints representing tile positions adjacent to this tile.
        """
        return self.adj

    def get_nearby(self):
        """
        Gets all the positions of nearby (adjacent + corner) tiles.
        :return: A List of tuples of two ints representing tile positions near to this tile.
        """
        return self.adj + self.cor