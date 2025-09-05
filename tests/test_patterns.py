import unittest
import numpy as np
from src.moire import patterns

class TestPatterns(unittest.TestCase):

    def setUp(self):
        """Set up common variables for tests."""
        self.shape = (100, 100)
        self.pitch = 20.0
        self.angle = 30.0
        self.lattice_constant = 30.0

    def test_generate_line_pattern_shape(self):
        """Test if the line pattern has the correct output shape."""
        pattern = patterns.generate_line_pattern(self.shape, self.pitch, self.angle)
        self.assertEqual(pattern.shape, self.shape)

    def test_generate_line_pattern_range(self):
        """Test if line pattern values are between 0 and 1."""
        pattern = patterns.generate_line_pattern(self.shape, self.pitch, self.angle)
        self.assertTrue(np.all(pattern >= 0.0))
        self.assertTrue(np.all(pattern <= 1.0))

    def test_generate_hex_pattern_shape(self):
        """Test if the hex pattern has the correct output shape."""
        pattern = patterns.generate_hex_pattern(self.shape, self.lattice_constant, self.angle)
        self.assertEqual(pattern.shape, self.shape)

    def test_generate_hex_pattern_range(self):
        """Test if hex pattern values are between 0 and 1."""
        pattern = patterns.generate_hex_pattern(self.shape, self.lattice_constant, self.angle)
        self.assertTrue(np.all(pattern >= 0.0))
        self.assertTrue(np.all(pattern <= 1.0))
        # The peak of the Gaussian should be 1.0 at the lattice points
        self.assertAlmostEqual(np.max(pattern), 1.0, places=3)