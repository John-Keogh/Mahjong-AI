import unittest
from tile_utils import is_set, Tile

class TestIsSetFunction(unittest.TestCase):
    def test_is_set(self):
        # Create three tiles with the same suit and rank
        tile1 = Tile(suit='stick', rank=1)
        tile2 = Tile(suit='stick', rank=1)
        tile3 = Tile(suit='stick', rank=1)
        
        # Call the is_set function with the three tiles
        result = is_set(tile1, tile2, tile3)
        
        # Check that the result is True (since all tiles have the same suit and rank)
        self.assertTrue(result)

    def test_is_not_set(self):
        # Create three tiles with different suits and ranks
        tile1 = Tile(suit='stick', rank=1)
        tile2 = Tile(suit='circle', rank=2)
        tile3 = Tile(suit='10k', rank=3)
        
        # Call the is_set function with the three tiles
        result = is_set(tile1, tile2, tile3)
        
        # Check that the result is False (since tiles have different suits and ranks)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
