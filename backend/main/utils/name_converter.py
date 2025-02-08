def to_java_name(python_name: str) -> str:
    """Convert Python snake_case to Java camelCase."""
    words = python_name.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:]) 