import random
from tile import Tile

import random
# random.seed(42)

import logging
from logging.handlers import RotatingFileHandler
import os

# Logging
logger = logging.getLogger("gamestate_logger")
logger.setLevel(logging.INFO)

log_file_path = "logs/gamestate_logging.log"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


# Define GameState class to represent the state of the game
class GameState:
    '''
    A class to represent the state of a Mahjong game
    '''
    def __init__(self):
        self.players = {
            'player1': [],
            'player2': [],
            'player3': [],
            'player4': []
        }

        # Define player as int
        self.players_to_int = {
            'player1': 0,
            'player2': 1,
            'player3': 2,
            'player4': 3
        }

        self.draw_pool = []
        self.discard_pool = []
        self.macro_direction = ['east', 'south', 'west', 'north']
        self.micro_direction = ['east', 'south', 'west', 'north']
        self.player_points = [50, 50, 50, 50]

        # Define game suits and ranks for one-hot encoding of tiles
        self.suits = ['stick', 'circle', '10k', 'red', 'green', 'white', 'east', 'south', 'west', 'north']
        self.ranks = list(range(1, 10))
        self.suit_to_idx = {suit: idx for idx, suit in enumerate(self.suits)}
        self.idx_to_suit = {idx: suit for idx, suit in enumerate(self.suits)}
        self.rank_to_idx = {rank: idx for idx, rank in enumerate(self.ranks)}
        self.idx_to_rank = {idx: rank for idx, rank in enumerate(self.ranks)}


        # Define one-hot encoding of directions
        self.macro_direction_to_idx = {macro_direction: idx for idx, macro_direction in enumerate(self.macro_direction)}
        self.micro_direction_to_idx = {micro_direction: idx for idx, micro_direction in enumerate(self.micro_direction)}


    def add_tile_to_hand(self, tile: Tile, player: str) -> None:
        '''
        Adds a tile to the specified player's hand
        '''
        if player not in self.players:
            logger.error(f"Error: cannot add tile to hand. Player {player} does not exist.")
            raise ValueError(f"Player {player} does not exist.")
        
        self.players[player].append(tile)


    def remove_tile_from_hand(self, tile: Tile, player: str) -> None:
        '''
        Removes a tile from the specified player's hand
        '''
        if player not in self.players:
            logger.error(f"Error: cannot remove tile from hand. Player {player} does not exist.")
            raise ValueError(f"Player {player} does not exist.")
        
        if tile not in self.players[player]:
            logger.error(f"Error: cannot remove tile from hand. Tile {tile} not found in {player}'s hand.")
            raise ValueError(f"Tile {tile} not found in {player}'s hand.")
        
        self.players[player].remove(tile)


    def clear_hand(self, player: str) -> None:
      '''
      Removes all tiles from the specified player's hand
      '''
      if len(self.players[player]) == 0:
          logger.debug('Player hand is already cleared.')
          return
      
      self.players[player].clear()
    


    def add_tile_to_draw_pool(self, tile: Tile) -> None:
        '''
        Adds a tile to the draw pool
        '''
        self.draw_pool.append(tile)


    def remove_tile_from_draw_pool(self, tile: Tile) -> None:
        '''
        Removes a tile from the draw pool
        '''
        if len(self.draw_pool) == 0:
            logger.debug('Cannot remove tile from draw pool because draw pool is empty.')
            return
        
        if tile not in self.draw_pool:
            logger.error('Cannot remove tile from draw pool because tile is not in draw pool.')
            raise ValueError(f"Tile {tile} not found in draw_pool.")
        
        self.draw_pool.remove(tile)


    def add_tile_to_discard_pool(self, tile: Tile) -> None:
        '''
        Adds a tile to the discard pool
        '''
        self.discard_pool.append(tile)


    def remove_tile_from_discard_pool(self, tile: Tile) -> None:
        '''
        Removes a tile from the discard pool
        '''
        if len(self.discard_pool) == 0:
            logger.debug('Cannot remove tile from discard pool because discard pool is empty.')
            return
        
        if tile not in self.discard_pool:
            logger.error('Cannot remove tile from discard pool because tile is not in discard pool.')
            raise ValueError(f"Tile {tile} not found in discard_pool.")
        
        self.discard_pool.remove(tile)


    def count(self, category: str) -> int:
        '''
        Counts the number of tiles in the specified game category
        '''
        categories = {
            'draw_pool': self.draw_pool,
            'discard_pool': self.discard_pool,
            **self.players
        }

        if category not in categories:
            logger.error(f"Cannot count '{category}' because Category '{category}' not found.")
            raise ValueError(f"Category '{category}' not found.")
        
        return len(categories[category])


    def sort_player_hand(self, player: str) -> None:
        '''
        Sorts the hand of the input player by suit and then rank
        '''
        # Get the player's hand
        player_hand = self.players.get(player, [])

        # Sort the player's hand
        sorted_hand = sorted(player_hand, key=lambda tile: (tile.suit, tile.rank))

        # Update the player's hand with the sorted version
        self.players[player] = sorted_hand


    def print_player_hand(self, player: str):
        '''
        Prints every tile in a player's hand

        Inputs:
        a string representing a key to the self.players dictionary (e.g. 'player1')
        '''
        for tile in self.players[player]:
            tile.display()


    def step_macro_direction(self) -> None:
        '''
        Updates the macro direction of the game
        '''
        self.macro_direction = [self.macro_direction[-1]] + self.macro_direction[:-1]


    def step_micro_direction(self) -> None:
        '''
        Updates the micro direction of the game
        '''
        self.micro_direction = [self.micro_direction[-1]] + self.micro_direction[:-1]


    def randomize_macro_direction(self) -> None:
        '''
        Shuffles the macrodirection of the game
        '''
        random.shuffle(self.macro_direction)


    def randomize_micro_direction(self) -> None:
        '''
        Shuffles the micro direction of the game
        '''
        random.shuffle(self.micro_direction)

    
    def initialize_draw_pool(self) -> None:
        '''
        Set up the game by adding all tiles to the draw pool and then shuffling them
        '''
        rank_suits = ['circle', 'stick', '10k']
        norank_suits = ['red', 'green', 'white', 'east', 'south', 'west', 'north']

        for suit in rank_suits:
            for rank in range(1, 10):
                for _ in range(4):
                    self.add_tile_to_draw_pool(Tile(suit, rank))
        
        for suit in norank_suits:
            for _ in range(4):
                self.add_tile_to_draw_pool(Tile(suit))

        random.shuffle(self.draw_pool)
    

    def deal_tiles(self) -> None:
        '''
        Deal tiles to each player at the start of the game
        '''
        if len(self.draw_pool) != 136:
            logger.error(f"Error: the draw pool does not contain the expected number of tiles (136).")
            raise ValueError(f"Draw pool not initialized correctly.")
        
        for _ in range(3):
            for player in self.players:
                for _ in range(4):
                    self.add_tile_to_hand(self.draw_pool[0], player)
                    self.remove_tile_from_draw_pool(self.draw_pool[0])
        
        for player in self.players:
            self.add_tile_to_hand(self.draw_pool[0], player)
            self.remove_tile_from_draw_pool(self.draw_pool[0])
        
        self.add_tile_to_hand(self.draw_pool[0], 'player1')
        self.remove_tile_from_draw_pool(self.draw_pool[0])