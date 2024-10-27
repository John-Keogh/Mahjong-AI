import logging
from logging.handlers import RotatingFileHandler

# Set up a dedicated logger for tile_utils
logger = logging.getLogger("tile_logger")
logger.setLevel(logging.ERROR)  # Set logging level

# Define handler with rotation settings
handler = RotatingFileHandler('tile_logging.log', maxBytes=10*1024*1024, backupCount=5)
handler.setLevel(logging.ERROR)  # Set logging level for this handler

# Set log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)

# Define Tile class to represent game pieces
class Tile:
    # Iniitialization
    def __init__(self, suit: str, rank: int=None):
        valid_suits = ['stick', 'circle', '10k', 'red', 'green', 'white', 'east', 'south', 'west', 'north']
        if suit in valid_suits:
            self.suit = suit
        else:
            logger.error(f"Error: {suit} is an invalid suit")
            raise ValueError(f"{suit} is an invalid suit")
        
        if rank is None or (isinstance(rank, int) and 1 <= rank <= 9):
            self.rank = rank
        else:
            logger.error(f"Error: {rank} is an invalid rank")
            raise ValueError(f"{rank} is an invalid rank")    
        
    # Customize representation for print statements to aid in debugging
    def __repr__(self):
        if self.rank:
            return f"{self.rank} {self.suit}"
        else:
            return f"{self.suit}"

    # Allow comparison of two Tile objects 
    def __eq__(self, other):
            if isinstance(other, Tile):
                if self.rank:
                    return self.suit == other.suit and self.rank == other.rank
                else:
                    return self.suit == other.suit
            return False

    # Allow tiles to be displayed via "tile.display()"
    def display(self):
        if self.rank:
            print(f"{self.rank} {self.suit}")
        else:
            print(f"{self.suit}")