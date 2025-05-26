from tile import Tile
from gamestate import GameState
from tile_utils import is_set, is_run, is_winning_hand, compute_score

import logging
from logging.handlers import RotatingFileHandler
import os

# Set up a dedicated logger for tile_utils
logger = logging.getLogger("player_utils_logger")
# level = logging.DEBUG # Set logging level
level = logging.ERROR
logger.setLevel(level)

# Define handler with rotation settings
handler = RotatingFileHandler('player_utils_logging.log', maxBytes=10*1024*1024, backupCount=5)
handler.setLevel(level)  # Set logging level for this handler

# Set log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)

# Logging
logger = logging.getLogger("player_utils_logger")
logger.setLevel(logging.INFO)

log_file_path = "logs/player_utils_logging.log"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


def pon_possible(gamestate: GameState, tile: Tile, player: str) -> bool:
    '''
    Determine if player can pon the most recently discarded tile

    Args:
    gamestate: Current state of the game
    tile: Tile class object
    player: 'player1', 'player2', etc.

    Returns:
    bool: True if player could pon tile; False if player could not pon tile
    '''
    count = 0
    player_hand = gamestate.players[player]
    for iter_tile in player_hand:
        if tile == iter_tile:
            count += 1

    if count > 1:
        return True
    else:
        return False


def pon(gamestate: GameState, tile: Tile, player: str) -> None:
    '''
    Adds the most recently discarded tile to player's hand (even if out of turn) to form a set

    Args:
    gamestate: Current state of the game
    tile: Tile class object
    player: 'player1', 'player2', etc.

    Returns:
    None
    '''
    if not pon_possible(gamestate, tile, player):
        logger.error(f"Error: {player} hand is ineligible to pon.")
        raise ValueError(f"{player} may not pon.")

    gamestate.add_tile_to_hand(tile, player)
    gamestate.remove_tile_from_discard_pool(tile)

    return


def gon_possible(gamestate: GameState, tile: Tile, player: str) -> bool:
    '''
    Determine if player can gon the most recently drawn tile

    Args:
    gamestate: Current state of the game
    tile: Tile class object
    player: 'player1', 'player2', etc.

    Returns:
    bool: True if player could pon tile; False if player could not pon tile
    '''
    if gamestate.players[player].count(tile) == 3:
        return True
    else:
        return False
    
def gon(gamestate: GameState, tile: Tile, player: str) -> None:
    '''
    Discards the most recently drawn tile
    Draws the tile from the back of the draw pool

    Args:
    gamestate: Current state of the game
    tile: Tile class object
    player: 'player1', 'player2', etc.

    Returns:
    None
    '''
    if not gon_possible(gamestate, tile, player):
        logger.error(f"Error: {player} hand is ineligible to gon.")
        raise ValueError(f"{player} may not gon.")

    gamestate.add_tile_to_discard_pool(tile)
    gamestate.remove_tile_from_hand(tile, player)
    last_tile = gamestate.draw_pool[-1]
    gamestate.add_tile_to_hand(last_tile, player)
    gamestate.draw_pool.pop()

    return


def eat_possible(gamestate: GameState, tile: Tile, player: str) -> bool:
    '''
    Determine if player can eat the most recently discarded tile

    Args:
    gamestate: Current state of the game
    tile: Tile class object
    player: 'player1', 'player2', etc.

    Returns:
    bool: True if player could eat tile; False if player could not eat tile
    '''
    eligible_tiles = []
    for iter_tile in gamestate.players[player]:
        if iter_tile.suit == tile.suit and abs(iter_tile.rank - tile.rank) <= 2:
            eligible_tiles.append(iter_tile)
    
    for tile_i in eligible_tiles:
        for tile_j in eligible_tiles:
            if is_run(tile_i, tile_j, tile):
                return True
    
    return False


def eat(gamestate: GameState, tile: Tile, player: str) -> None:
    '''
    Draws the tile that was most recently discarded
    Removes that tile from the draw pool

    Args:
    gamestate: Current state of the game
    tile: Tile class object
    player: 'player1', 'player2', etc.

    Returns:
    None
    '''
    if not eat_possible(gamestate, tile, player):
        logger.error(f"Error: {player} is ineligible to eat.")
        raise ValueError(f"{player} may not eat.")
    
    gamestate.add_tile_to_hand(tile, player)
    gamestate.remove_tile_from_discard_pool(tile)

    return