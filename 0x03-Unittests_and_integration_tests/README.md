# Utils Testing Project

This project contains utility functions and their corresponding unit tests, following Python best practices and coding standards.

## Project Structure

```
.
├── README.md
├── utils.py
└── test_utils.py
```

## Files Description

### `utils.py`
Contains utility functions for working with nested data structures:
- `access_nested_map()`: Function to access values in nested dictionaries using a path tuple

### `test_utils.py`
Unit tests for the utils module:
- `TestAccessNestedMap`: Test class for testing the `access_nested_map` function
- Uses parameterized testing to test multiple input scenarios

## Requirements

- Python 3.7+ (tested on Ubuntu 18.04 LTS)
- `parameterized` library for parameterized testing

## Installation

1. Clone or download this project
2. Install the required dependencies:
   ```bash
   pip install parameterized
   ```

## Usage

### Running the Tests

To run all unit tests:
```bash
python test_utils.py
```

To run tests with verbose output:
```bash
python test_utils.py -v
```

### Using the Utils Module

```python
from utils import access_nested_map

# Example usage
nested_data = {"a": {"b": {"c": 42}}}
result = access_nested_map(nested_data, ("a", "b", "c"))
print(result)  # Output: 42
```

## Code Standards

This project follows:
- PEP 8 coding style (enforced by pycodestyle version 2.5)
- Type annotations for all functions
- Comprehensive docstrings for modules, classes, and functions
- Executable file permissions
- Proper shebang lines (`#!/usr/bin/env python`)

## Testing

The project uses the `unittest` framework with `parameterized` decorators for efficient testing of multiple input scenarios. The test suite includes:

- Basic nested dictionary access
- Multi-level nested dictionary traversal
- Edge cases and various input combinations

## Contributing

When contributing to this project, please ensure:
- All code follows pycodestyle guidelines
- All functions have type annotations
- All modules, classes, and functions have proper documentation
- New features include corresponding unit tests