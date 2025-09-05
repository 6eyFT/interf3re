import unittest
from src.moire import utils

class TestUtils(unittest.TestCase):

    def test_parse_layer_def_valid(self):
        """Test parsing of a valid layer string."""
        layer_str = "type=lines; pitch=15.5; angle=45"
        expected = {'type': 'lines', 'pitch': 15.5, 'angle': 45.0}
        self.assertEqual(utils.parse_layer_def(layer_str), expected)

    def test_parse_layer_def_no_float(self):
        """Test a string with a non-float value."""
        layer_str = "type=hex"
        expected = {'type': 'hex'}
        self.assertEqual(utils.parse_layer_def(layer_str), expected)
        
    def test_parse_layer_def_malformed(self):
        """Test that a malformed string returns None."""
        layer_str = "type=lines, pitch=10"
        self.assertIsNone(utils.parse_layer_def(layer_str))
        
    def test_parse_layer_def_empty(self):
        """Test that an empty string returns an empty dictionary."""
        layer_str = ""
        self.assertEqual(utils.parse_layer_def(layer_str), {})