import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from src.moire import engine

class TestEngine(unittest.TestCase):

    def test_normalize_pattern(self):
        """Test the normalization function with various inputs."""
        # Test a standard range
        pattern1 = np.array([0, 5, 10])
        np.testing.assert_allclose(engine.normalize_pattern(pattern1), [0.0, 0.5, 1.0])

        # Test an already normalized range
        pattern2 = np.array([0.0, 0.25, 1.0])
        np.testing.assert_allclose(engine.normalize_pattern(pattern2), [0.0, 0.25, 1.0])

        # Test a flat pattern (should avoid division by zero)
        pattern3 = np.array([5, 5, 5])
        np.testing.assert_allclose(engine.normalize_pattern(pattern3), [5, 5, 5])

    @patch('src.moire.engine.save_static_2d')
    def test_generate_pattern_calls_2d_render(self, mock_save_2d):
        """Verify the engine calls the 2D render function."""
        args = MagicMock()
        args.resolution = 100
        # The 'dimension' attribute is no longer used, but we can leave it for mock completeness
        args.dimension = '2d' 
        args.layer = ["type=lines;pitch=10;angle=0"]

        engine.generate_pattern(args)

        # The only assertion needed is that the 2D save function is called.
        mock_save_2d.assert_called_once()
        
        # Check that the second argument passed to the mock is a numpy array
        call_args, _ = mock_save_2d.call_args
        self.assertIsInstance(call_args[1], np.ndarray)