#!/usr/bin/env python3
"""
Utility functions module.
This module provides utility functions for working with nested data structures
and other common operations.
"""

from typing import Dict, Tuple, Any, Union


def access_nested_map(nested_map: Dict[str, Any], path: Tuple[str, ...]) -> Any:
   
    current = nested_map
    for key in path:
        current = current[key]
    return current