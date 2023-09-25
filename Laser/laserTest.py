import unittest
from laser import laser

class TestLaser(unittest.TestCase):
    def setUp(self):
        self.l = laser("COM3", 1)

    def test_combineBytes(self):
        self.assertEqual(self.l.combineBytes([0b10110100, 0b01110010]),
                          0b01101001110010)
        
    def test_combineBytes_len(self):
        self.assertLessEqual(self.l.combineBytes([0b11111111, 0b01111111]).bit_length(),
                         14)
        
    def test_distance50(self):
        self.assertAlmostEqual(self.l.distance(8184), 50, places=2)

    def test_distance0(self):
        self.assertAlmostEqual(self.l.distance(161), 0, places=2)

    def test_distance100(self):
        self.assertAlmostEqual(self.l.distance(16207), 100, places=2)
        
if __name__ == '__main__':

    unittest.main()