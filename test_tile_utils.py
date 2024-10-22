import unittest
from tile_utils import is_set, is_run, is_winning_hand, compute_score, Tile, GameState

import logging
# Set warning level
# level = logging.DEBUG
level = logging.ERROR
logging.basicConfig(filename = 'tile_utils_logging.log', level=level, format='%(asctime)s - %(levelname)s - %(message)s')


class TestIsSetFunction(unittest.TestCase):
    def test_is_set_3_true(self):
        # Create three tiles with the same suit and rank
        tile1 = Tile(suit='stick', rank=1)
        tile2 = Tile(suit='stick', rank=1)
        tile3 = Tile(suit='stick', rank=1)
        
        # Call the is_set function with the three tiles
        result = is_set(tile1, tile2, tile3)
        
        # Check that the result is True (since all tiles have the same suit and rank)
        self.assertTrue(result)


    def test_is_set_2_true(self):
        # Create three tiles with the same suit and rank
        tile1 = Tile(suit='stick', rank=1)
        tile2 = Tile(suit='stick', rank=1)
        
        # Call the is_set function with the three tiles
        result = is_set(tile1, tile2)
        
        # Check that the result is True (since all tiles have the same suit and rank)
        self.assertTrue(result)


    def test_is_set_4_true(self):
        # Create three tiles with the same suit and rank
        tile1 = Tile(suit='stick', rank=1)
        tile2 = Tile(suit='stick', rank=1)
        tile3 = Tile(suit='stick', rank=1)
        tile4 = Tile(suit='stick', rank=1)
        
        # Call the is_set function with the three tiles
        result = is_set(tile1, tile2, tile3, tile4)
        
        # Check that the result is True (since all tiles have the same suit and rank)
        self.assertTrue(result)


    def test_is_set_1_false(self):
        # Create three tiles with the same suit and rank
        tile1 = Tile(suit='stick', rank=1)
        
        # Call the is_set function with the three tiles
        result = is_set(tile1)
        
        # Check that the result is True (since all tiles have the same suit and rank)
        self.assertFalse(result)


    def test_is_set_false(self):
        tile1 = Tile(suit='stick', rank=1)
        tile2 = Tile(suit='stick', rank=1)
        tile3 = Tile(suit='stick', rank=1)
        group = [tile1, tile2, tile3]
        
        result = is_set(group)
        self.assertTrue(result)


    def test_is_set_list_true(self):
        tile1 = Tile(suit='stick', rank=1)
        tile2 = Tile(suit='circle', rank=2)
        tile3 = Tile(suit='north')
        
        result = is_set(tile1, tile2, tile3)
        self.assertFalse(result)


    def test_is_run_true(self):
        tile1 = Tile(suit='10k', rank=1)
        tile2 = Tile(suit='10k', rank=2)
        tile3 = Tile(suit='10k', rank=3)

        result = is_run(tile1, tile2, tile3)
        self.assertTrue(result)


    def test_is_run_false(self):
        tile1 = Tile(suit='10k', rank=1)
        tile2 = Tile(suit='10k', rank=2)
        tile3 = Tile(suit='10k', rank=4)

        result = is_run(tile1, tile2, tile3)
        self.assertFalse(result)


    def test_is_run_set_false(self):
        tile1 = Tile(suit='green')
        tile2 = Tile(suit='green')
        tile3 = Tile(suit='green')

        result = is_run(tile1, tile2, tile3)
        self.assertFalse(result)


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


    def test_is_winning_hand_false(self):
        gamestate = GameState()
        player = 'player1'

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('east'),
            Tile('east'),
            Tile('east'),
            Tile('stick', 8),
            Tile('stick', 8),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('stick', 9),
            Tile('stick', 9),
            Tile('circle', 4),
            Tile('circle', 3)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        result, _ = is_winning_hand(gamestate, player)
        self.assertFalse(result)


    def test_score_2(self):
        '''
        Test lowest possible player hand score
        '''
        gamestate = GameState()
        player = 'player1'
        expected_score = 2

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('circle', 1),
            Tile('circle', 1),
            Tile('circle', 1),
            Tile('stick', 8),
            Tile('stick', 8),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('stick', 9),
            Tile('stick', 9),
            Tile('circle', 4),
            Tile('circle', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)
        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_5(self):
        '''
        Test whether all tiles with ranks are of the same suit
        (e.g. only sticks or circles or 10ks)
        
        A winning hand that has all of the same suit adds 3 to player score
        '''
        gamestate = GameState()
        player = 'player1'
        expected_score = 5

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
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_6(self):
        '''
        Test whether all tiles with ranks are of the same suit
        (e.g. only sticks or circles or 10ks with colors and directions)
        
        A winning hand that has all of the same suit adds 3 to player score

        If the hand has a set of colors or valid directions, that adds 1 to the score as well
        '''
        gamestate = GameState()
        player = 'player1'
        expected_score = 6

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('green'),
            Tile('green'),
            Tile('green'),
            Tile('stick', 9),
            Tile('stick', 9),
            Tile('stick', 9),
            Tile('stick', 4),
            Tile('stick', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_sets(self):
        '''
        Test whether all groups of tiles being sets results in the correct score
        
        A winning hand that has groups of exclusively sets is worth an additional 3 points

        This test includes a set of colors which adds an additional 1 point
        (Assume the direction is invald towards additional points)

        Total expected score is 2 + 3 + 1 = 6
        '''
        gamestate = GameState()
        player = 'player1'
        expected_score = 6

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('10k', 1),
            Tile('10k', 1),
            Tile('10k', 1),
            Tile('green'),
            Tile('green'),
            Tile('green'),
            Tile('west'),
            Tile('west'),
            Tile('west'),
            Tile('stick', 4),
            Tile('stick', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_runs(self):
        '''
        Test whether all groups of tiles being runs results in the correct score
        
        A winning hand that has groups of exclusively runs is worth an additional 1 points

        This test includes a set of colors which adds an additional 1 point
        (Assume the direction is invald towards additional points)

        Total expected score is 2 + 1 + 1 = 4
        '''
        gamestate = GameState()
        player = 'player1'
        expected_score = 4

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('10k', 1),
            Tile('10k', 2),
            Tile('10k', 3),
            Tile('green'),
            Tile('green'),
            Tile('green'),
            Tile('west'),
            Tile('west'),
            Tile('west'),
            Tile('stick', 4),
            Tile('stick', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_direction_macro_valid(self):
        '''
        Test whether a winning hand with a valid macro direction is appropriately awarded an additional point
        
        Total expected score is 2 + 1 = 3

        Note that 'player2' is used, because the default macro direction is east for all players
        (e.g. gamestate.macro_direction[0] = 'east')
        But the default micro direction is east for player 1, not player 2
        '''
        gamestate = GameState()
        player = 'player2'
        expected_score = 3

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('10k', 1),
            Tile('10k', 2),
            Tile('10k', 3),
            Tile('circle', 2),
            Tile('circle', 2),
            Tile('circle', 2),
            Tile('east'),
            Tile('east'),
            Tile('east'),
            Tile('stick', 4),
            Tile('stick', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_direction_invalid(self):
        '''
        Test that a winning hand with an invalid direction is not awarded additional points

        Total expected score is 2

        Note that 'west' is used in the hand because it is neither the default macro direction nor the default direction for 'player1'
        '''
        gamestate = GameState()
        player = 'player1'
        expected_score = 2

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('10k', 1),
            Tile('10k', 2),
            Tile('10k', 3),
            Tile('circle', 2),
            Tile('circle', 2),
            Tile('circle', 2),
            Tile('west'),
            Tile('west'),
            Tile('west'),
            Tile('stick', 4),
            Tile('stick', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_direction_micro_valid(self):
        '''
        Test that a winning hand with a valid micro direction is awarded an additional point

        Total expected score is 2 + 1 = 3

        Note that 'player3' and 'west' are used in this test because 'west' is not the default macro direction, but it is the default micro direction for player 3
        '''
        gamestate = GameState()
        player = 'player3'
        expected_score = 3

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('10k', 1),
            Tile('10k', 2),
            Tile('10k', 3),
            Tile('circle', 2),
            Tile('circle', 2),
            Tile('circle', 2),
            Tile('west'),
            Tile('west'),
            Tile('west'),
            Tile('stick', 4),
            Tile('stick', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_direction_micro_macro_valid(self):
        '''
        Test that a winning hand with a valid macro and micro direction is awarded additional points

        Total expected score is 2 + 1 + 1 = 4

        Note that 'player1' and 'east' are used in this test because 'east' is the default macro and micro direction for player 1
        '''
        gamestate = GameState()
        player = 'player1'
        expected_score = 4

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('10k', 1),
            Tile('10k', 2),
            Tile('10k', 3),
            Tile('circle', 2),
            Tile('circle', 2),
            Tile('circle', 2),
            Tile('east'),
            Tile('east'),
            Tile('east'),
            Tile('stick', 4),
            Tile('stick', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_direction_micro_macro_valid_2(self):
        '''
        Test that a winning hand with a valid macro and micro direction is awarded additional points

        Total expected score is 2 + 1 + 1 = 4

        Note that 'player2', 'east', and 'south' are used in this test because 'east' is the default macro direction for all players and 'south' is the default direction for player 2
        '''
        gamestate = GameState()
        player = 'player2'
        expected_score = 4

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('10k', 1),
            Tile('10k', 2),
            Tile('10k', 3),
            Tile('south'),
            Tile('south'),
            Tile('south'),
            Tile('east'),
            Tile('east'),
            Tile('east'),
            Tile('stick', 4),
            Tile('stick', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_direction_double(self):
        '''
        Test that a winning hand with a double that is comprised of a direction yields the minimum winning points (2)

        Total expected score is 2

        Note that the hand is comprised of sets, colors, and directions, which would otherwise award additional points
        '''
        gamestate = GameState()
        player = 'player1'
        expected_score = 2

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('10k', 1),
            Tile('10k', 1),
            Tile('10k', 1),
            Tile('south'),
            Tile('south'),
            Tile('south'),
            Tile('red'),
            Tile('red'),
            Tile('red'),
            Tile('east'),
            Tile('east')
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_color_double(self):
        '''
        Test that a winning hand with a double that is comprised of a color yields the minimum winning points (2)

        Total expected score is 2

        Note that the hand is comprised of sets, colors, and directions, which would otherwise award additional points
        '''
        gamestate = GameState()
        player = 'player1'
        expected_score = 2

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('stick', 1),
            Tile('10k', 1),
            Tile('10k', 1),
            Tile('10k', 1),
            Tile('south'),
            Tile('south'),
            Tile('south'),
            Tile('red'),
            Tile('red'),
            Tile('red'),
            Tile('white'),
            Tile('white')
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)


    def test_score_misc_edge(self):
        '''
        Test that a hand chosen by Amy returns the expected score.
        '''
        gamestate = GameState()
        player = 'player1'
        expected_score = 3

        manual_tiles = [
            Tile('stick', 4),
            Tile('stick', 4),
            Tile('stick', 4),
            Tile('circle', 7),
            Tile('circle', 8),
            Tile('circle', 9),
            Tile('south'),
            Tile('south'),
            Tile('south'),
            Tile('east'),
            Tile('east'),
            Tile('east'),
            Tile('10k', 1),
            Tile('10k', 1)

        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        score = compute_score(gamestate, player)

        result = (score == expected_score)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
