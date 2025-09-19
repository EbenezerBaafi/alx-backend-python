#!/usr/bin/env python
"""
Utility functions module.

This module provides utility functions for working with nested data structures
and other common operations.
"""

from typing import Dict, Tuple, Any, Union


def access_nested_map(nested_map: Dict[str, Any], path: Tuple[str, ...]) -> Any:
    """
    Access a nested map using a sequence of keys.
    
    This function traverses a nested dictionary structure using the provided
    path tuple to access deeply nested values.
    
    Args:
        nested_map (Dict[str, Any]): The nested dictionary to traverse
        path (Tuple[str, ...]): A tuple of keys representing the path to the value
        
    Returns:
        Any: The value found at the specified path
        
    Raises:
        KeyError: If any key in the path is not found or if trying to access
                  a key on a non-dictionary value
    """
    current = nested_map
    for key in path:
        if not isinstance(current, dict):
            raise KeyError(key)
        current = current[key]
    return current