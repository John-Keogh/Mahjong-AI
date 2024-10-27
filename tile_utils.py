from tile import Tile
from gamestate import GameState
import itertools
import copy

import logging
from logging.handlers import RotatingFileHandler

# Set up a dedicated logger for tile_utils
logger = logging.getLogger("tile_utils_logger")
logger.setLevel(logging.ERROR)  # Set logging level

# Define handler with rotation settings
handler = RotatingFileHandler('tile_utils_logging.log', maxBytes=10*1024*1024, backupCount=5)
handler.setLevel(logging.ERROR)  # Set logging level for this handler

# Set log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)


# Method to check if three tiles form a set
def is_set(*args) -> bool:
    '''
    Checks whether 2, 3, or 4 input tiles form a set (same suit and rank)
    
    Inputs:
    2, 3, or 4 variables of the Tile class as individual inputs or as a group of tiles

    Returns:
    Boolean
    '''
    try:
        # Check whether input is a group of tiles or individual tiles
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            tiles = args[0]
        else:
            tiles = args

        # Check whether input tiles is empty
        if not tiles:
            logging.error('Error: input to is_set function is empty.')       
            return False
        
        # Check that there are only 2, 3, or 4 tiles
        if len(tiles) not in {2, 3, 4}:
            logging.warning('Error: input to is_set function does not contain 2, 3, or 4 tiles.')  
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


# Features to add:
# 1) handle sets with multiple win conditions
def is_winning_hand(gamestate: GameState, player: str):
    '''
    Checks whether a player's hand meets any win conditions

    Inputs:
    gamestate - state of the game
    player - key to GameState players dictionary (e.g. 'player1')

    Returns:
    is_winning - boolean
    grouped_hand - the winning hand grouped into sets
        e.g. ((1 circle, 1 circle, 1 circle), (1 stick, 2 stick, 3 stick), (8 stick, 8 stick, 8 stick), (9 stick, 9 stick, 9 stick), (4 circle, 4 circle))
    '''
    if not isinstance(player, str):
        logging.error(f"Error: player input {player} is not a string.")
        raise ValueError(f"Player input {player} is not a string.")
    
    if player not in gamestate.players:
        logging.error(f"Error: cannot retrieve player hand. Player {player} does not exist.")
        raise ValueError(f"Player {player} does not exist.")
    
    # Initialize return values
    is_winning = False
    combination = []

    # Sort and retrieve player hand
    gamestate.sort_player_hand(player)
    player_hand = copy.deepcopy(gamestate.players[player])

    # Generate a list of all valid runs/sets
    groups = list(itertools.combinations(player_hand, 3))
    valid_groups = []
    for group in groups:
        # if is_set(*group):
        if is_set(group[0], group[1], group[2]):
            valid_groups.append(group)
        elif is_run(group[0], group[1], group[2]):
            valid_groups.append(group)
    
    # Check if there are enough valid groups to form a winning hand
    if len(valid_groups) < 4:
        logging.debug("len(valid_groups) < 4")
        return is_winning, None
    
    # Generate all combinations of four groups
    combinations = list(itertools.combinations(valid_groups, 4))

    # Check all possible combinations of four groups for a valid winning hand
    for grouped_hand in combinations:
        # Reset player_hand for each check
        player_hand = copy.deepcopy(gamestate.players[player])

        # Boolean controls whether or not to check for final double
        win_possible = True

        # Flatten combination of four groups
        flattened_hand = [tile for group in grouped_hand for tile in group]

        # Check whether the combination of four groups can be made using tiles in player_hand (i.e. no repeat tiles used)
        for tile in flattened_hand:
            if tile in player_hand:
                player_hand.remove(tile)
            else:
                win_possible = False
                break
        
        # Check whether final two tiles are identical
        if win_possible and is_set(player_hand[0], player_hand[1]):
            is_winning = True
            # Add the last two tiles as a group of two to combination
            double = (player_hand[0], player_hand[1])
            grouped_hand += (double,)
            return is_winning, grouped_hand
    
    return is_winning, grouped_hand

def compute_score(gamestate: GameState, player: str) -> int:
    '''
    Computes score of a player's hand

    Inputs:
    gamestate - state of the game
    player - key to GameState players dictionary (e.g. 'player1')

    Returns:
    score - integer representing the score of a player's hand
    '''
    if not isinstance(player, str):
        logging.error(f"Error: player input {player} is not a string.")
        raise ValueError(f"Player input {player} is not a string.")
    
    if player not in gamestate.players:
        logging.error(f"Error: cannot retrieve player hand. Player {player} does not exist.")
        raise ValueError(f"Player {player} does not exist.")
    
    is_winning, grouped_hand = is_winning_hand(gamestate, player)

    if not is_winning:
        score = 0
        return score

    # Initialize score - a winning hand has a base value of 2 points
    score = 2

    rank_suits = ['stick', 'circle', '10k']
    color_suits = ['red', 'green', 'white']
    direction_suits = ['east', 'south', 'west', 'north']

    ####################################################################################################################
    # Score check 1 - check whether all tiles with ranks are of the same suit
    # Initializations
    same_suit = False
    suit = None
    num_groups = 0
    count = 0

    # Count the number of groups that have suits and select a suit to compare against
    for group in grouped_hand:
        if group[0].suit in rank_suits:
            num_groups += 1
            suit = group[0].suit

    # Check whether all tiles with ranks have the same suits
    if suit != None:
        for group in grouped_hand:
            if group[0].suit == suit:
                count += 1 
    if count == num_groups:
        same_suit = True

    # Add 3 points to the score if all tiles with ranks have the same suit
    if same_suit:
        score += 3

    ####################################################################################################################
    # Score check 2 - check whether all groups are sets/runs
    # If all groups are sets, add 3 points to the score
    # If all groups are runs, add 1 point to the score
    sets_runs = []
    for group in grouped_hand:
        if (len(group) != 2
            and group[0].suit in rank_suits):
            if is_set(*group):
                sets_runs.append('set')
            else:
                sets_runs.append('run')
    
    if all(x == sets_runs[0] for x in sets_runs):
        # Add 3 points if all groups are sets
        if sets_runs[0] == 'set':
            score += 3
        # Add 1 point if all groups are runs
        else:
            score += 1

    ####################################################################################################################
    # Score check 3 - check whether any groups are colors
    for group in grouped_hand:
        if group[0].suit in color_suits:
            if len(group) == 2:
                score = 2
                return score
            else:
                score += 1
    
    ####################################################################################################################
    # Score check 4 - check for directions
    for group in grouped_hand:
        if group[0].suit in direction_suits:
            if len(group) == 2:
                score = 2
                return score
            if group[0].suit == gamestate.macro_direction[0]:
                score += 1
            if group[0].suit == gamestate.micro_direction[player]:
                score += 1

    return score
