# Import Tile class from tile.py file
from tile import Tile

import logging
# Set warning level
# level = logging.DEBUG
level = logging.WARNING
logging.basicConfig(filename = 'tile_utils_logging.log', level=level, format='%(asctime)s - %(levelname)s - %(message)s')

# Method to check if three tiles form a set
def is_set(*tiles) -> bool:
    '''
    Checks whether 2, 3, or 4 input tiles form a set (same suit and rank)
    
    Inputs:
    2, 3, or 4 variables of the Tile class

    Returns:
    Boolean
    '''
    try:
        # Check whether input tiles is empty
        if not tiles:
            logging.error('Error: input to is_set function is empty.')       
            return False
        
        # Check that there are only 2, 3, or 4 tiles
        if len(tiles) not in {2, 3, 4}:
            logging.error('Error: input to is_set function does not contain 2, 3, or 4 tiles.')  
            return False
        
        # Check that all tiles are of the Tile class
        if not all(isinstance(tile, Tile) for tile in tiles):
            logging.error('Error: input to is_set function is not of the Tile class.')
            return False

        first_tile = tiles[0]
        same_suit = all(tile.suit == first_tile.suit for tile in tiles)
        same_rank = all(tile.rank == first_tile.rank for tile in tiles)

        # Return boolean for all tiles being of same suit and same rank
        return same_suit and same_rank
    
    except Exception as e:
        logging.error(e)
        return False


# Method to check if three tiles form a run
def is_run(tile1: Tile, tile2: Tile, tile3: Tile) -> bool:
    '''
    Checks whether 3 input tiles form a run (same suit, consecutive ranks)
    
    Inputs:
    3 variables of the Tile class

    Returns:
    Boolean
    '''
    try:
        # Check that all tiles are of the Tile class
        if not (isinstance(tile1, Tile) and isinstance(tile2, Tile) and isinstance(tile3, Tile)):
            logging.error('Error: one or more inputs to is_run function is not of the Tile class.')
            return False
        
        # Check that all tiles are of the same suit
        if not(tile1.suit == tile2.suit == tile3.suit):
            logging.debug(f"Tiles have different suits: {tile1.suit}, {tile2.suit}, {tile3.suit}")
            return False
        
        # Check that the tiles are eligible to form a run (that they have a rank)
        if (tile1.rank == None
            or tile2.rank == None
            or tile3.rank == None):
            logging.debug(f"One or more tiles do not have a rank.")
            return False
        
        # Sort the tiles by rank
        sorted_tiles = sorted([tile1, tile2, tile3], key=lambda tile: tile.rank)

        # Check that the tiles are consecutive
        if (sorted_tiles[1].rank == sorted_tiles[0].rank + 1 and
                sorted_tiles[2].rank == sorted_tiles[0].rank + 2):
            return True
        else:
            logging.debug("Tiles are not consecutive: "
                            f"{sorted_tiles[0].rank}, {sorted_tiles[1].rank}, {sorted_tiles[2].rank}")
            return False
    
    except Exception as e:
        logging.error(e)
        return False