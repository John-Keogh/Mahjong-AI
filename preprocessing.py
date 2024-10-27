import numpy as np
from tile import Tile
import torch
from gamestate import GameState

def encode_tile(gamestate: GameState, tile: Tile) -> np.ndarray:
    '''
    Encode a tile with one-hot encoding

    Args:
    tile: object of Tile class with suit and rank

    Returns:
    tile_encoding: a numpy vector of 19 zeros/ones to represent the tile suit and rank
    '''
    if tile.suit not in gamestate.suits:
        raise ValueError(f"Invalid tile suit: {tile.suit}")
    
    if tile.rank not in gamestate.ranks and tile.rank is not None:
        raise ValueError(f"Invalid tile rank: {tile.rank}")

    suit_vector = np.zeros(len(gamestate.suits))  # 10 total suits
    rank_vector = np.zeros(len(gamestate.ranks))   # 9 total ranks
    
    suit_vector[gamestate.suit_to_idx[tile.suit]] = 1

    if tile.rank is not None:
        rank_vector[gamestate.rank_to_idx[tile.rank]] = 1

    tile_encoding = np.concatenate([suit_vector, rank_vector])
    return tile_encoding

def encode_tile_batch(gamestate: GameState, tiles: list[Tile]):
    '''
    Encode a batch of tiles with one-hot encoding

    Args:
    tiles: list of Tile class objects

    Returns:
    tile_encodings_tensor: a PyTorch tensor where each row is the encoding of a tile
    '''
    tile_encodings = np.array([encode_tile(gamestate, tile) for tile in tiles])
    tile_encodings_tensor = torch.from_numpy(tile_encodings).float()
    return tile_encodings_tensor

def encode_macro_direction(gamestate: GameState):
    '''
    Encode the macro game direction with one-hot encoding

    Args:
    gamestate: object of GameState class

    Returns:
    macro_direction_encoding: a PyTorch tensor of 4 zeros/ones to represent the macro game direction
    '''
    macro_direction_encoding = np.zeros(4)
    macro_direction = gamestate.macro_direction[0]

    macro_direction_encoding[gamestate.macro_direction_to_idx[macro_direction]] = 1
    macro_direction_tensor = torch.from_numpy(macro_direction_encoding).float()
    return macro_direction_tensor

def encode_micro_direction(gamestate: GameState):
    '''
    Encode the micro game direction with one-hot encoding

    Args:
    gamestate: object of GameState class

    Returns:
    macro_direction_encoding: a numpy vector of 4 zeros/ones to represent the micro game direction
    '''
    micro_direction_encoding = np.zeros(4)
    micro_direction = gamestate.micro_direction[0]

    micro_direction_encoding[gamestate.micro_direction_to_idx[micro_direction]] = 1
    micro_direction_tensor = torch.from_numpy(micro_direction_encoding).float()
    return micro_direction_tensor


def prepare_input(gamestate: GameState, player: str):
    '''
    Compiles the following information to prepare for network input:
    1) Tiles in player's hand
    2) Tiles in the discard pool
    3) Tiles in the draw pool
    4) Macro game direction
    5) Micro game direction

    Args:
    gamestate: object of GameState class
    player: 'player1', 'player2', etc.

    Returns:
    input_tensor: a PyTorch tensor representing all information available to player
    '''
    # 1) Tiles in player's hand
    tiles_in_hand = []
    for tile in gamestate.players[player]:
        tiles_in_hand.append(tile)
    tiles_in_hand_tensor = encode_tile_batch(gamestate, tiles_in_hand)
    tiles_in_hand_tensor = torch.flatten(tiles_in_hand_tensor)
    # print(f"tiles_in_hand_tensor = \n{tiles_in_hand_tensor}")

    # 2) Tiles in discard pool
    tiles_in_discard_pool = []
    for tile in gamestate.discard_pool:
        tiles_in_discard_pool.append(tile)
    tiles_in_discard_pool_tensor = encode_tile_batch(gamestate, tiles_in_discard_pool)
    # print(f"tiles_in_discard_pool_tensor = \n{tiles_in_discard_pool_tensor}")

    # 3) Tiles in draw pool (one-hot encoding of all zeros)
    tiles_not_in_hand = 136 - 14 - 3*13 # 136 total tiles, 14 in player's hand, 13 in all other players' hands
    tiles_in_draw_pool = tiles_not_in_hand - len(tiles_in_discard_pool)
    tiles_in_draw_pool_tensor = torch.zeros(tiles_in_draw_pool * 19) # 19 one-hot values per tile
    # print(f"tiles_in_draw_pool_tensor = \n{tiles_in_draw_pool_tensor}")

    # 4) Macro game direction
    macro_direction_tensor = encode_macro_direction(gamestate)
    # print(f"macro_direction_tensor = \n{macro_direction_tensor}")

    # 5) Micro game direction
    micro_direction_tensor = encode_micro_direction(gamestate)
    # print(f"micro_direction_tensor = \n{micro_direction_tensor}")

    input_tensor = torch.hstack((tiles_in_hand_tensor, tiles_in_discard_pool_tensor, tiles_in_draw_pool_tensor, macro_direction_tensor, micro_direction_tensor))

    return input_tensor