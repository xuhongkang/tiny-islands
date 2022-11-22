from enum import Enum


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
