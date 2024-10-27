import unittest

from player_utils import pon_possible, pon, gon_possible, gon, eat_possible, eat, Tile, GameState

class TestIsSetFunction(unittest.TestCase):
    def test_pon_possible_true(self):
        '''
        Test that a tile eligible to be pon'd returns True using the pon_possible function
        '''
        gamestate = GameState()
        player = 'player1'

        test_tile = Tile('10k', 1)

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('south'),
            Tile('10k', 1),
            Tile('10k', 1)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        result = pon_possible(gamestate, test_tile, player)
        self.assertTrue(result)


    def test_pon_possible_false(self):
        '''
        Test that a tile ineligible to be pon'd returns False using the pon_possible function
        '''
        gamestate = GameState()
        player = 'player1'

        test_tile = Tile('stick', 1)

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('south'),
            Tile('10k', 1),
            Tile('10k', 1)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        result = pon_possible(gamestate, test_tile, player)
        self.assertFalse(result)


    def test_pon_true(self):
        '''
        Test that the pon function operates correctly:
        1) Add the tile at the end of the discard pool to the player's hand
        2) Remove the tile at the end of the discard pool from the discard pool
        '''
        gamestate = GameState()
        player = 'player1'
        test_tile = Tile('10k', 1)
        
        gamestate.add_tile_to_discard_pool(test_tile)
        
        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('south'),
            Tile('10k', 1),
            Tile('10k', 1)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        try:
            pon(gamestate, test_tile, player)
        except ValueError as e:
            print(f"Caught an error: {e}")

        if gamestate.players[player].count(test_tile) == 3 and test_tile not in gamestate.discard_pool:
            result = True
        else:
            result = False
        self.assertTrue(result)


    def test_pon_false(self):
        '''
        Test that the pon function properly disallows pon when invalid:
        '''
        gamestate = GameState()
        player = 'player1'
        test_tile = Tile('circle', 1)
        result = False
        
        gamestate.add_tile_to_discard_pool(test_tile)
        
        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('south'),
            Tile('10k', 1),
            Tile('10k', 1)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        try:
            pon(gamestate, test_tile, player)
        except ValueError:
            result = True

        self.assertTrue(result)


    def test_gon_possible_true(self):
        '''
        Test that a tile eligible to be gon'd returns True using the gon_possible function
        '''
        gamestate = GameState()
        player = 'player1'

        test_tile = Tile('10k', 1)

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('10k', 1),
            Tile('10k', 1),
            Tile('10k', 1)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        result = gon_possible(gamestate, test_tile, player)
        self.assertTrue(result)


    def test_gon_possible_false(self):
        '''
        Test that a tile ineligible to be gon'd returns False using the gon_possible function
        '''
        gamestate = GameState()
        player = 'player1'

        test_tile = Tile('stick', 1)

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('south'),
            Tile('10k', 1),
            Tile('10k', 1)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)
        
        result = gon_possible(gamestate, test_tile, player)
        self.assertFalse(result)


    def test_gon_true(self):
        '''
        Test that the gon function operates correctly:
        1) Discard the tile being gon'd
        2) Add the card from the back of the discard pool to player's hand
        3) Remove the last card from the back of the discard pool
        '''
        gamestate = GameState()
        player = 'player1'
        test_tile = Tile('10k', 1)

        tile1 = Tile('north')
        tile2 = Tile('white')
        gamestate.add_tile_to_draw_pool(tile1)
        gamestate.add_tile_to_draw_pool(tile2)
        
        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('10k', 1),
            Tile('10k', 1),
            Tile('10k', 1)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        try:
            gon(gamestate, test_tile, player)
        except ValueError as e:
            print(f"Caught an error: {e}")

        if test_tile in gamestate.discard_pool and tile2 in gamestate.players[player] and tile2 not in gamestate.draw_pool:
            result = True
        else:
            result = False
        self.assertTrue(result)


    def test_gon_false(self):
        '''
        Test that the gon function properly disallows gon when invalid:
        '''
        gamestate = GameState()
        player = 'player1'
        test_tile = Tile('circle', 1)
        result = False
        
        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('south'),
            Tile('10k', 1),
            Tile('10k', 1)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        try:
            gon(gamestate, test_tile, player)
        except ValueError:
            result = True

        self.assertTrue(result)


    def test_eat_possible_true(self):
        '''
        Test that a tile eligible to be eaten returns True using the eat_possible function
        '''
        gamestate = GameState()
        player = 'player1'

        test_tile = Tile('10k', 3)

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('south'),
            Tile('10k', 1),
            Tile('10k', 2)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        result = eat_possible(gamestate, test_tile, player)
        self.assertTrue(result)


    def test_eat_possible_false(self):
        '''
        Test that a tile ineligible to be eaten returns False using the eat_possible function
        '''
        gamestate = GameState()
        player = 'player1'

        test_tile = Tile('10k', 3)

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('south'),
            Tile('10k', 1),
            Tile('10k', 4)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        result = eat_possible(gamestate, test_tile, player)
        self.assertFalse(result)


    def test_eat_true(self):
        '''
        Test that the eat function works properly:
        1) Adds tile to player hand
        2) Removes tile from discard pool
        '''
        gamestate = GameState()
        player = 'player1'

        test_tile = Tile('10k', 3)
        gamestate.add_tile_to_discard_pool(test_tile)

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('south'),
            Tile('10k', 1),
            Tile('10k', 2)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        try:
            eat(gamestate, test_tile, player)
        except ValueError as e:
            print(f"Caught an error: {e}")

        if test_tile in gamestate.players[player] and test_tile not in gamestate.discard_pool:
            result = True
        else:
            result = False

        self.assertTrue(result)


    def test_eat_false(self):
        '''
        Test that the eat function properly disallows eat when invalid:
        '''
        gamestate = GameState()
        player = 'player1'

        test_tile = Tile('10k', 3)
        result = False

        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3),
            Tile('stick', 4),
            Tile('stick', 5),
            Tile('stick', 6),
            Tile('stick', 7),
            Tile('stick', 8),
            Tile('stick', 9),
            Tile('east'),
            Tile('west'),
            Tile('south'),
            Tile('10k', 1),
            Tile('10k', 1)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        try:
            eat(gamestate, test_tile, player)
        except ValueError:
            result = True

        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
