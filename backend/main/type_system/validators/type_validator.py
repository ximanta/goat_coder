import json
from pathlib import Path
from ..exceptions import TypeValidationError
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class TypeValidator:
    ALLOWED_PYTHON_TYPES = {
        'int', 'str', 'bool',
        'List[int]', 'List[str]', 'List[bool]'
    }
    
    ALLOWED_JAVA_TYPES = {
        'int', 'String', 'boolean',
        'int[]', 'String[]', 'boolean[]'
    }

    def __init__(self):
        self.config_path = Path(__file__).parent.parent / "config"
        self.java_types = self._load_config("java_types.json")
        self.python_types = self._load_config("python_types.json")
        self.type_conversions = self._load_config("type_conversions.json")

    def _load_config(self, filename: str) -> dict:
        try:
            with (self.config_path / filename).open() as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {filename}: {str(e)}")
            raise TypeValidationError(f"Failed to load type configuration: {str(e)}")

    def validate_type(self, type_str: str, language: str) -> bool:
        """Validate if a type is valid for a given language"""
        try:
            if language == "java":
                return (
                    type_str in self.java_types["primitive_types"]["numeric"] or
                    type_str in self.java_types["primitive_types"]["text"] or
                    type_str in self.java_types["primitive_types"]["boolean"] or
                    type_str in self.java_types["wrapper_types"]["numeric"] or
                    type_str in self.java_types["wrapper_types"]["text"] or
                    type_str in self.java_types["wrapper_types"]["boolean"] or
                    self._is_valid_array_type(type_str, "java")
                )
            elif language == "python":
                return (
                    type_str in self.python_types["basic_types"]["numeric"] or
                    type_str in self.python_types["basic_types"]["text"] or
                    type_str in self.python_types["basic_types"]["boolean"] or
                    self._is_valid_collection_type(type_str, "python")
                )
            return False
        except Exception as e:
            logger.error(f"Error validating type {type_str} for {language}: {str(e)}")
            raise TypeValidationError(f"Type validation failed: {str(e)}")

    def _is_valid_array_type(self, type_str: str, language: str) -> bool:
        """Check if the type is a valid array type"""
        if language == "java":
            # Check for Java array syntax (e.g., int[], String[])
            base_type = type_str.replace("[]", "")
            return self.validate_type(base_type, language)
        return False

    def _is_valid_collection_type(self, type_str: str, language: str) -> bool:
        """Check if the type is a valid collection type"""
        if language == "python":
            # Check for Python collection syntax (e.g., List[int], Optional[str])
            if type_str.startswith(("List[", "Optional[")):
                inner_type = type_str[type_str.find("[")+1:type_str.find("]")]
                return self.validate_type(inner_type, language)
        return False

    def validate_structure(self, structure: Dict, language: str) -> bool:
        allowed_types = self.ALLOWED_PYTHON_TYPES if language == "python" else self.ALLOWED_JAVA_TYPES
        
        for input_field in structure['input_structure']:
            field_type = input_field['Input Field'].split()[0]
            if field_type not in allowed_types:
                raise TypeValidationError(f"Invalid type: {field_type}. Allowed types: {allowed_types}")
                
        output_type = structure['output_structure']['Output Field'].split()[0]
        if output_type not in allowed_types:
            raise TypeValidationError(f"Invalid type: {output_type}. Allowed types: {allowed_types}")
            
        return True 