#!/usr/bin/env python
"""
Unit tests for utils module.

This module contains unit tests for the utils.access_nested_map function
using the unittest framework with parameterized testing.
"""

import unittest
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for access_nested_map function.
    
    This class contains unit tests to verify that access_nested_map
    correctly retrieves values from nested dictionary structures
    using the provided path tuples.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the correct value for given inputs.
        
        Args:
            nested_map (dict): The nested dictionary to access
            path (tuple): The path tuple specifying the keys to traverse
            expected: The expected return value
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that access_nested_map raises KeyError for invalid paths.
        
        Args:
            nested_map (dict): The nested dictionary to access
            path (tuple): The invalid path tuple that should raise KeyError
        """
        with self.assertRaises(KeyError) as context:
            utils.access_nested_map(nested_map, path)
        
        # Check that the exception message contains the missing key
        missing_key = path[0] if not nested_map else path[-1]
        self.assertIn(str(missing_key), str(context.exception))


if __name__ == '__main__':
    unittest.main()