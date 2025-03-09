import json
import os
from typing import Dict, Any

class JavaTypeMapper:
    """A type mapper specifically for converting Python types to Java types."""
    
    def __init__(self):
        self.type_mappings = self._load_type_mappings()

    def _load_type_mappings(self) -> Dict[str, Any]:
        """Load Java type mappings from the JSON configuration file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_file = os.path.join(current_dir, "java_type_mappings.json")
        
        with open(mapping_file, "r") as f:
            return json.load(f)

    def to_java_type(self, python_type: str) -> str:
        """Convert Python type notation to Java type notation."""
        python_type = python_type.strip().lower()  # Normalize to lowercase

        # Handle List types
        if python_type.startswith(("list[", "List[")):
            inner_type = python_type[5:-1]  # Remove 'List[' and ']'
            if "union[" in inner_type:
                return "List<Object>"
            elif "dict[" in inner_type or "list[" in inner_type:
                return f"List<{self.to_java_type(inner_type)}>"
            array_type = self.type_mappings.get(f"List[{inner_type}]")
            if array_type:
                return array_type
            return f"{self.to_java_type(inner_type)}[]"

        # Handle Dict types
        if python_type.startswith(("dict[", "Dict[")):
            # If it contains a Union type anywhere, return Object
            if "union[" in python_type:
                return "Object"
                
            inner_types = python_type[5:-1].split(",")  # Remove 'Dict[' and ']', then split
            if len(inner_types) == 2:
                key_type = inner_types[0].strip()
                value_type = inner_types[1].strip()
                
                # Handle complex value types
                if "[" in value_type:  # Nested collections
                    value_type = self.to_java_type(value_type)
                else:
                    # Use wrapper type for Map values
                    value_type = self.get_wrapper_type(value_type)
                
                # Handle key type (usually String in Java Maps)
                if "[" in key_type:
                    key_type = "String"
                else:
                    key_type = self.get_wrapper_type(key_type)
                
                return f"Map<{key_type}, {value_type}>"
            return "Map<String, Object>"

        # Handle Union types
        if "union[" in python_type:
            return "Object"

        # Handle Dict without type parameters
        if python_type in ["dict", "Dict"]:
            return "Object"

        # Handle basic types
        return self.type_mappings.get(python_type, "Object")

    def get_wrapper_type(self, primitive_type: str) -> str:
        """Get the Java wrapper type for a primitive type."""
        wrapper_type = self.type_mappings.get("_wrapper", {}).get(primitive_type.lower())
        if wrapper_type:
            return wrapper_type
        # If no wrapper type found, try basic type mapping
        return self.type_mappings.get(primitive_type.lower(), primitive_type)
