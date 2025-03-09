"""
Type mapping system for converting between different programming languages.
Currently supports:
- Java: Converts Python types to Java types
"""

from .java.java_type_mapper import JavaTypeMapper

__all__ = ['JavaTypeMapper']