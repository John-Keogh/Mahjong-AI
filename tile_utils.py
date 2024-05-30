# Import Tile class from tile.py file
from tile import Tile
from gamestate import GameState
import itertools

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


# Features to add:
# 1) handle sets of 4/hands with more than 14 tiles
# 2) handle sets with multiple win conditions
def is_winning_hand(gamestate: GameState, player: str):
    '''
    Checks whether a player's hand meets any win conditions

    Inputs:
    gamestate - state of the game
    player - key to GameState players dictionary (e.g. 'player1')

    Returns:
    is_winning - boolean
    combinations -  a set of groups that comprise the winning hand
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
    player_hand = gamestate.players[player]

    # Generate a list of all valid runs/sets
    groups = list(itertools.combinations(player_hand, 3))
    valid_groups = []
    for group in groups:
        # if is_set(*group):
        if is_set(group[0], group[1], group[2]):
            valid_groups.append(group)

        if is_run(group[0], group[1], group[2]):
            valid_groups.append(group)
    
    # Check if there are enough valid groups to form a winning hand
    if len(valid_groups) < 4:
        return is_winning, None
    
    # Generate all combinations of four groups
    combinations = list(itertools.combinations(valid_groups, 4))

    # Check all possible combinations of four groups for a valid winning hand
    for combination in combinations:
        # Boolean controls whether or not to check for final double
        win_possible = True

        # Flatten combination of four groups
        flattened_hand = [tile for group in combination for tile in group]

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
            return is_winning, combination
    
    return is_winning, None

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
    
    is_winning, combination = is_winning_hand(gamestate, player)

    print(f"is_winning = {is_winning}")
    print('')

    if not is_winning:
        score = 0
        return score
    
    gamestate.print_player_hand(player)
    
    # Add double to combination
    double = []
    temp_hand = gamestate.players[player][:]
    # for tile in [tile for group in combination for tile in group]:
    #     temp_hand.remove(tile)
    for group in combination:
        for tile in group:
            if tile not in temp_hand:
                logging.debug(f"Error: tile {tile} not in player hand.")
            temp_hand.remove(tile)

    for tile in temp_hand:
        double.append(tile)
    
    combination += (tuple(double),)

    # Initialize score - a winning hand is worth at least 2 points
    score = 2
    gamestate.sort_player_hand[player]
    hand = gamestate.players[player]

    rank_suits = ['stick', 'circle', '10k']
    color_suits = ['red', 'green', 'white']
    direction_suits = ['east', 'south', 'west', 'north']

    # Score check 1 - check whether all tiles with ranks are of the same suit
    # Find the suit of the first tile that isn't a direction or color
    same_suit = False
    for tile in hand:
        if tile.suit in rank_suits:
            suit = tile.suit
            break
    count = 0
    # Check whether all tiles with ranks have the same suits
    for group in combination:
        if (group[0].suit != suit
            and group[0].suit in rank_suits):
            break
        if count == len(combination) - 1:
            same_suit == True
            count += 1
    
    # Add 3 points to the score if all tiles with ranks have the same suit
    if same_suit:
        score += 3

    # Score check 2 - check whether all tiles are sets/runs
    sets_runs = []
    for group in combination:
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

    # Score check 3 - check whether any groups are colors
    for group in combination:
        if group[0].suit in color_suits:
            score += 1
    
    # Score check 4 - check for directions
    for group in combination:
        if group[0].suit in direction_suits:
            if len(group == 2):
                break
            if group[0].suit == gamestate.macro_direction[0]:
                score += 1
            if group[0].suit == gamestate.micro_direction[0]:
                score += 1

    return score

