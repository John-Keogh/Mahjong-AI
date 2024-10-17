import unittest
from tile_utils import is_set, is_run, is_winning_hand, compute_score, Tile, GameState

import logging
# Set warning level
# level = logging.DEBUG
level = logging.ERROR
logging.basicConfig(filename = 'tile_utils_logging.log', level=level, format='%(asctime)s - %(levelname)s - %(message)s')


class TestIsSetFunction(unittest.TestCase):
    # def test_is_set_3_true(self):
    #     # Create three tiles with the same suit and rank
    #     tile1 = Tile(suit='stick', rank=1)
    #     tile2 = Tile(suit='stick', rank=1)
    #     tile3 = Tile(suit='stick', rank=1)
        
    #     # Call the is_set function with the three tiles
    #     result = is_set(tile1, tile2, tile3)
        
    #     # Check that the result is True (since all tiles have the same suit and rank)
    #     self.assertTrue(result)

    # def test_is_set_2_true(self):
    #     # Create three tiles with the same suit and rank
    #     tile1 = Tile(suit='stick', rank=1)
    #     tile2 = Tile(suit='stick', rank=1)
        
    #     # Call the is_set function with the three tiles
    #     result = is_set(tile1, tile2)
        
    #     # Check that the result is True (since all tiles have the same suit and rank)
    #     self.assertTrue(result)

    # def test_is_set_4_true(self):
    #     # Create three tiles with the same suit and rank
    #     tile1 = Tile(suit='stick', rank=1)
    #     tile2 = Tile(suit='stick', rank=1)
    #     tile3 = Tile(suit='stick', rank=1)
    #     tile4 = Tile(suit='stick', rank=1)
        
    #     # Call the is_set function with the three tiles
    #     result = is_set(tile1, tile2, tile3, tile4)
        
    #     # Check that the result is True (since all tiles have the same suit and rank)
    #     self.assertTrue(result)

    # def test_is_set_1_false(self):
    #     # Create three tiles with the same suit and rank
    #     tile1 = Tile(suit='stick', rank=1)
        
    #     # Call the is_set function with the three tiles
    #     result = is_set(tile1)
        
    #     # Check that the result is True (since all tiles have the same suit and rank)
    #     self.assertFalse(result)

    # def test_is_set_false(self):
    #     tile1 = Tile(suit='stick', rank=1)
    #     tile2 = Tile(suit='stick', rank=1)
    #     tile3 = Tile(suit='stick', rank=1)
    #     group = [tile1, tile2, tile3]
        
    #     result = is_set(group)
    #     self.assertTrue(result)

    # def test_is_set_list_true(self):
    #     tile1 = Tile(suit='stick', rank=1)
    #     tile2 = Tile(suit='circle', rank=2)
    #     tile3 = Tile(suit='north')
        
    #     result = is_set(tile1, tile2, tile3)
    #     self.assertFalse(result)

    # def test_is_run_true(self):
    #     tile1 = Tile(suit='10k', rank=1)
    #     tile2 = Tile(suit='10k', rank=2)
    #     tile3 = Tile(suit='10k', rank=3)

    #     result = is_run(tile1, tile2, tile3)
    #     self.assertTrue(result)

    # def test_is_run_false(self):
    #     tile1 = Tile(suit='10k', rank=1)
    #     tile2 = Tile(suit='10k', rank=2)
    #     tile3 = Tile(suit='10k', rank=4)

    #     result = is_run(tile1, tile2, tile3)
    #     self.assertFalse(result)

    # def test_is_run_set_false(self):
    #     tile1 = Tile(suit='green')
    #     tile2 = Tile(suit='green')
    #     tile3 = Tile(suit='green')

    #     result = is_run(tile1, tile2, tile3)
    #     self.assertFalse(result)

    def test_is_winning_hand_true(self):
        gamestate = GameState()
        player = 'player1'

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 8),
            Tile('stick', 8),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('stick', 9),
            Tile('stick', 9),
            Tile('stick', 4),
            Tile('stick', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        result, _ = is_winning_hand(gamestate, player)
        self.assertTrue(result)

    # def test_is_winning_hand_false(self):
    #     gamestate = GameState()
    #     player = 'player1'

    #     manual_tiles = [
    #         Tile('stick', 1),
    #         Tile('stick', 2),
    #         Tile('stick', 3),
    #         Tile('east'),
    #         Tile('east'),
    #         Tile('east'),
    #         Tile('stick', 8),
    #         Tile('stick', 8),
    #         Tile('stick', 8),
    #         Tile('stick', 9),
    #         Tile('stick', 9),
    #         Tile('stick', 9),
    #         Tile('circle', 4),
    #         Tile('circle', 3)
    #     ]

    #     for tile in manual_tiles:
    #         gamestate.add_tile_to_hand(tile, player)
        
        result, _ = is_winning_hand(gamestate, player)
        self.assertFalse(result)

    def test_score_2(self):
        '''
        Test lowest possible player hand score
        '''
        gamestate = GameState()
        player = 'player1'

    #     manual_tiles = [
    #         Tile('stick', 1),
    #         Tile('stick', 2),
    #         Tile('stick', 3),
    #         Tile('circle', 1),
    #         Tile('circle', 1),
    #         Tile('circle', 1),
    #         Tile('stick', 8),
    #         Tile('stick', 8),
    #         Tile('stick', 8),
    #         Tile('stick', 9),
    #         Tile('stick', 9),
    #         Tile('stick', 9),
    #         Tile('circle', 4),
    #         Tile('circle', 4)
    #     ]

    #     for tile in manual_tiles:
    #         gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)
        result = (score == 2)
        self.assertTrue(result)

    # def test_score_5(self):
    #     '''
    #     Test whether all tiles with ranks are of the same suit
    #     (e.g. only sticks or circles or 10ks with colors and directions)
        
    #     A winning hand that has all of the same suit adds 3 to player score
    #     '''

    #     gamestate = GameState()
    #     player = 'player1'

    #     manual_tiles = [
    #         Tile('stick', 1),
    #         Tile('stick', 2),
    #         Tile('stick', 3),
    #         Tile('stick', 1),
    #         Tile('stick', 1),
    #         Tile('stick', 1),
    #         Tile('stick', 8),
    #         Tile('stick', 8),
    #         Tile('stick', 8),
    #         Tile('stick', 9),
    #         Tile('stick', 9),
    #         Tile('stick', 9),
    #         Tile('stick', 4),
    #         Tile('stick', 4)
    #     ]

    #     for tile in manual_tiles:
    #         gamestate.add_tile_to_hand(tile, player)
        
    #     score = compute_score(gamestate, player)

    #     result = (score == 5)
    #     self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
