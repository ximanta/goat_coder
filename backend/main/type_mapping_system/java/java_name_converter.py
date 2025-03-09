"""
Module for converting Python names to Java naming conventions.
Part of the centralized type mapping system.
"""

import re

def to_java_name(python_name: str) -> str:
    """Convert Python snake_case to Java camelCase.
    
    If the name is already in camelCase, it will be preserved.
    
    Args:
        python_name (str): Name in Python snake_case or Java camelCase format
        
    Returns:
        str: Name in Java camelCase format
        
    Raises:
        ValueError: If the input string is empty, contains only underscores,
                   contains whitespace, or contains invalid special characters
    """
    # Input validation
    if not python_name:
        raise ValueError("Name cannot be empty")
    
    if python_name.isspace() or '\n' in python_name or '\t' in python_name:
        raise ValueError("Name cannot contain whitespace")
        
    # Check for invalid special characters (allow only letters, numbers, and underscores)
    if not re.match(r'^[a-zA-Z0-9_]+$', python_name):
        raise ValueError("Name can only contain letters, numbers, and underscores")
    
    if python_name.strip('_') == '':
        raise ValueError("Name cannot contain only underscores")

    # If name is already in camelCase (no underscores), preserve it
    if '_' not in python_name:
        return python_name

    # Remove leading and trailing underscores
    python_name = python_name.strip('_')
    
    # Split by underscores and filter out empty strings
    words = [word for word in python_name.split('_') if word]
    
    if not words:
        raise ValueError("Name cannot be empty after processing")
    
    # Convert to lowercase for consistent processing
    words = [word.lower() for word in words]
    
    # Capitalize all words except the first one
    return words[0] + ''.join(word.capitalize() for word in words[1:])
