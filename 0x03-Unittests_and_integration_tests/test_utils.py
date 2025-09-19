#!/usr/bin/env python3
"""
Unit tests for utils module.

This module contains unit tests for the utils.access_nested_map function
using the unittest framework with parameterized testing.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for access_nested_map function
    
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
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()