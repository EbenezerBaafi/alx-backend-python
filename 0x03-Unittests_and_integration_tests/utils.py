#!/usr/bin/env python3
"""
Utility functions module.

This module provides utility functions for working with nested data structures
and other common operations.
"""

from typing import Dict, Tuple, Any, Union, Callable
import requests
from functools import wraps


def access_nested_map(nested_map: Dict[str, Any], path: Tuple[str, ...]) -> Any:
    """
    Access a nested map using a sequence of keys.

    This function traverses a nested dictionary structure using the provided
    path tuple to access deeply nested values.

    Args:
        nested_map (Dict[str, Any]): The nested dictionary to traverse
        path (Tuple[str, ...]): A tuple of keys representing the path to the
                                value

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


def get_json(url: str) -> Dict[str, Any]:
    """
    Get JSON data from a remote URL.

    This function makes an HTTP GET request to the specified URL and
    returns the JSON response as a dictionary.

    Args:
        url (str): The URL to fetch JSON data from

    Returns:
        Dict[str, Any]: The JSON data as a dictionary

    Raises:
        requests.RequestException: If the HTTP request fails
        ValueError: If the response is not valid JSON
    """
    response = requests.get(url)
    return response.json()


def memoize(func: Callable) -> Callable:
    """
    Decorator that caches the result of method calls.

    This decorator caches the return value of a method so that subsequent
    calls with the same arguments return the cached result without
    re-executing the method.

    Args:
        func (Callable): The function to be memoized

    Returns:
        Callable: The wrapped function with memoization
    """
    @wraps(func)
    def wrapper(self):
        if not hasattr(self, '_memoize_cache'):
            self._memoize_cache = {}
        if func.__name__ not in self._memoize_cache:
            self._memoize_cache[func.__name__] = func(self)
        return self._memoize_cache[func.__name__]
    return wrapper