from enum import Enum
from typing import Callable


class Terrain(Enum):
    """
    Enum representing types of Terrain.
    """
    EMPTY = 0
    BOATS = 1
    WAVES = 2
    BEACH = 3
    HOUSES = 4
    CHURCHES = 5
    FOREST = 6
    MOUNTAIN = 7

    LAND_TERRAIN = {HOUSES, CHURCHES, FOREST, MOUNTAIN}
    SEA_TERRAIN = {BOATS, WAVES}


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


def _generate_adjacency_info(pos: tuple[int, int]) -> (list[tuple[int, int]], list[tuple[int, int]]):
    """
    Static Helper Method for generating valid adjacency info.
    :param pos: A tuple of two ints representing the position from which to generate adjacency info.
    :return: A tuple of two list of ints representing touching tiles and nearby tiles.
    """
    pos_x, pos_y = pos
    adj, cor = list(), list()
    if pos_x < 8:
        adj.append(pos_x + 1, pos_y)
    if pos_x > 0:
        adj.append(pos_x - 1, pos_y)
    if pos_y < 8:
        adj.append(pos_x, pos_y - 1)
    if pos_y > 0:
        adj.append(pos_x, pos_y - 1)
    if pos_x < 8 and pos_y < 8:
        cor.append(pos_x + 1, pos_y + 1)
    if pos_x < 8 and pos_y > 0:
        cor.append(pos_x + 1, pos_y - 1)
    if pos_x > 0 and pos_y < 8:
        cor.append(pos_x - 1, pos_y + 1)
    if pos_x > 0 and pos_y > 0:
        cor.append(pos_x - 1, pos_y - 1)
    return adj, cor


class Board:
    def __int__(self):
        """
        Constructor for the board.
        """
        self.grid, self.islands = dict(), tuple([], [], [])
        for pos_y in range(9):
            for pos_x in range(9):
                pos = (pos_x, pos_y)
                adj, cor = _generate_adjacency_info(pos)
                self.grid[pos] = Tile(adj, cor)

    def _get_tile_at(self, pos: tuple[int, int]) -> Tile:
        """
        Helper Method for getting the tile at a given position.
        :param pos: A tuple of two ints representing the target position.
        :return: A Tile representing the tile at the given position.
        :exception: If the target position does not exist in board.
        """
        if pos not in self.grid:
            raise Exception("Invalid Position: Target Position Does Not Exist In Board.")
        return self.grid[pos]

    def _get_tiles_at(self, lop: list[tuple[int, int]]) -> list[Tile]:
        """
        Helper Method for getting all the tiles given a list of positions.
        :param lop: A list of tuple of two ints representing a list of target positions.
        :return: A list of tiles representing the tiles at the given position.
        :exception: If any target position does not exist in board.
        """
        lot = list()
        for pos in lop:
            lot.append(self._get_tile_at(pos))
        return lot

    def _get_nearby_tiles(self, pos: tuple[int, int]) -> list[Tile]:
        """
        Helper Method for getting all nearby tiles given a single position.
        :param pos: A tuple of two ints representing the target position.
        :return: A list of tiles representing all nearby tiles.
        """
        tile, lot = self._get_tile_at(pos), list()
        for nearby_pos in tile.get_nearby():
            lot.append(self._get_tile_at(nearby_pos))
        return lot

    def _count_filter_upon_nearby_tiles(self, pos: tuple[int, int], func: Callable[[Tile], bool]) -> int:
        """
        Helper Method for calling a method on all nearby tiles and returning a count.
        :param pos: A tuple of two ints representing the target position.
        :return: An int representing the count of tiles that have the method return true.
        """
        tile, count = self._get_tile_at(pos), 0
        for nearby_pos in tile.get_nearby():
            nearby_tile = self._get_tile_at(nearby_pos)
            if func(nearby_tile):
                count += 1
        return count

    def _count_filter_upon_touching_tiles(self, pos: tuple[int, int], func: Callable[[Tile], bool]) -> int:
        """
        Helper Method for calling a method on all touching tiles and returning a count.
        :param pos: A tuple of two ints representing the target position.
        :return: An int representing the count of tiles that have the method return true.
        """
        tile, count = self._get_tile_at(pos), 0
        for adj_pos in tile.get_nearby():
            adj_tile = self._get_tile_at(adj_pos)
            if func(adj_tile):
                count += 1
        return count

    def _get_touching_tiles(self, pos: tuple[int, int]) -> list[Tile]:
        """
        Helper Method for getting all touching tiles given a single position.
        :param pos: A tuple of two ints representing the target position.
        :return: A list of tiles representing all touching tiles.
        """
        tile, lot = self._get_tile_at(pos), list()
        for adj_pos in tile.get_touching():
            lot.append(self._get_tile_at(adj_pos))
        return lot

    def _check_sec_wave_in_rc(self, pos: tuple[int, int]) -> bool:
        """
        Helper Method for checking if there's another wave in the same row or column
        :param pos: A tuple of two ints representing the target position from which to search.
        :return: True if there's another wave. False if otherwise.
        """
        pos_x, pos_y = pos
        for c in range(9):
            if c != pos_x:
                tile = self._get_tile_at((c, pos_y))
                if tile.get_terrain() == Terrain.WAVES:
                    return True
        for r in range(9):
            if r != pos_y:
                tile = self._get_tile_at((pos_x, r))
                if tile.get_terrain() == Terrain.WAVES:
                    return True
        return False

    def _get_distance_to_island(self, pos: tuple[int, int], temp: bool) -> int:
        """
        Helper method for calculating the shortest distance to any island close by using bfs.
        :param pos: A tuple of two ints representing the target position from which to search.
        :param temp: A boolean representing whether we should take into account land terrains tiles who haven't been
        put on an island yet.
        :return: An int representing the shortest distance to any island.
        """
        visited, queue = list(), list()
        visited.append(pos)
        queue.append(pos)
        while queue:
            next_pos = queue.pop(0)
            next_tile = self._get_tile_at(next_pos)
            if (temp and next_tile.get_terrain() in Terrain.LAND_TERRAIN) or (not temp and next_tile.is_on_island()):
                return abs(next_pos[0] - pos[0]) + abs(next_pos[1] - pos[1])
            for neighbor in next_tile.get_touching():
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)
        return 0

    def _is_on_shore(self, pos: tuple[int, int]) -> bool:
        """
        Helper Method for checking if a tile at the given position is on the shore (near but not on an island)
        :param pos: A tuple of two ints representing the target position from which to search.
        :return: True if the tile is on the shore, False if otherwise.
        """
        return not self._get_tile_at(pos).is_on_island() and \
            self._count_filter_upon_touching_tiles(pos, lambda tile: tile.is_on_island()) >= 1

    def _is_tile_valid(self, pos: tuple[int, int], temp: bool) -> bool:
        """
        Helper Method for checking if the tile at the given position satisfies game rules.
        :param pos:A tuple of two ints representing the position of the target tile.
        :param temp: A boolean representing whether we should take into account land terrains tiles who haven't been
        put on an island yet.
        :return: True if the tile is valid, False if otherwise.
        """
        tile = self._get_tile_at(pos)
        terrain = tile.get_terrain()
        if terrain in Terrain.LAND_TERRAIN:
            if not temp and not tile.is_on_island():
                return False
        elif terrain in Terrain.SEA_TERRAIN and tile.is_on_island():
            return False
        elif terrain == Terrain.BEACH:
            if not temp and self._is_on_shore(pos):
                return False
        return True

    def _get_all_tiles_on_same_island(self, pos: tuple[int, int]) -> list[Tile]:
        """
        Helper Method for getting all the tiles on the same island.
        :param pos:A tuple of two ints representing the position of the target tile.
        :return: A list of tiles representing all tiles on the same island.
        """
        for island in self.islands:
            if pos in island:
                return [self._get_tile_at(x) for x in island]
        return list()

    def get_score_at(self, pos: tuple[int, int], temp: bool) -> int:
        """
        Calculates the score of a single tile at a given position.
        :param pos: A tuple of two ints representing the target position from which to calculate the score.
        :param temp: A boolean representing whether we should take into account land terrains tiles who haven't been
        put on an island yet.
        :return: An int representing the score of a tile, -5 if invalid,
        positive points if valid (different based on type).
        """
        tile = self._get_tile_at(pos)
        terrain = tile.get_terrain()
        if not temp and not self._is_tile_valid(pos):
            return -5
        if terrain == Terrain.BOATS:
            return self._get_distance_to_island(pos, False)
        elif terrain == Terrain.WAVES:
            return 0 if self._check_sec_wave_in_rc(pos) else 2
        elif terrain == Terrain.BEACH:
            return self._count_filter_upon_touching_tiles(pos, lambda t: t.is_on_island())
        elif terrain == Terrain.HOUSES:
            terrains = [x.get_terrain() for x in self._get_nearby_tiles(pos)
                        if x.get_terrain() != Terrain.EMPTY and x.get_terrain() != Terrain.HOUSES]
            return len(set(terrains))
        elif terrain == Terrain.CHURCHES:
            score = 0
            score += 2 * self._count_filter_upon_nearby_tiles(pos, lambda t: t.get_terrain() == Terrain.HOUSES)
            if not temp:
                island_tiles = [x for x in self._get_all_tiles_on_same_island(pos)
                                if x not in self._get_nearby_tiles(pos)]
                for i_tile in island_tiles:
                    i_terrain = i_tile.get_terrain()
                    if i_terrain == Terrain.HOUSES:
                        score += 1
                    elif i_terrain == Terrain.CHURCHES:
                        return 0
            return score
        elif terrain == Terrain.FOREST:
            return 2 if self._count_filter_upon_touching_tiles(pos, lambda t: t.get_terrain() == Terrain.FOREST) > 0 \
                else 0
        elif terrain == Terrain.MOUNTAIN:
            return 2 * self._count_filter_upon_nearby_tiles(pos, lambda t: t.get_terrain() == Terrain.FOREST)

    def add_terrain(self, pos: tuple[int, int], terrain: Terrain):
        """
        Adds the given terrain to the tile on the given position in the board.
        :param pos: A tuple of two non-negative ints representing the position of the target tile.
        :param terrain: A Terrain representing the target terrain to add.
        :exception: If the target position does not exist in board.
        :exception: If the target position is invalid or if the tile's terrain at that position has already been set.
        """
        target_tile = self._get_tile_at(pos)
        target_tile.set_terrain(terrain)

    def _are_islands_full(self) -> bool:
        """
        Helper Method for determining if all the three islands have been drawn.
        :return: True if they have all been drawn, false if otherwise.
        """
        for island in self.islands:
            if not island:
                return False
        return True

    def _get_island_with_shore_positions(self, island: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Helper Method for getting all the extended occupying positions of an island, including the shore.
        :param island: A list of tuples of two non-negative ints representing the positions consisting of the island.
        :return: A list of tuple of two non-negative ints representing the positions of an island plus its shore.
        """
        lop = set()
        for pos in island:
            lop.add(self._get_tile_at(pos).get_nearby())
        return island + list(lop)

    def add_island(self, lop: list[tuple[int, int]]):
        """
        Adds a well-formed list of island positions to the board representation, toggling the on island variable of
        related tiles (on and off).
        :param lop: is a list of tuples of two non-negative integers representing the position of the target
        island tiles.
        :exception: If all islands have been drawn or the provided island positions are in conflict with existing island
        positions.
        """
        if self._are_islands_full():
            raise Exception("All Islands have been Drawn.")
        for island in self.islands:
            if island:
                if not set(self._get_island_with_shore_positions(island)).isdisjoint(lop):
                    raise Exception("Invalid Tiles, Either Already Part of an Island or Part of Existing Shore.")
            else:
                for tile in self._get_tiles_at(lop):
                    tile.toggle_on_island()
                island.extend(lop)
