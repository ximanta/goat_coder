import json
from pathlib import Path
from ..exceptions import TypeConversionError
import logging

logger = logging.getLogger(__name__)

class TypeConverter:
    def __init__(self):
        self.config_path = Path(__file__).parent.parent / "config"
        self.type_conversions = self._load_config("type_conversions.json")

    def _load_config(self, filename: str) -> dict:
        try:
            with (self.config_path / filename).open() as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {filename}: {str(e)}")
            raise TypeConversionError(f"Failed to load type configuration: {str(e)}")

    def convert_type(self, type_str: str, from_lang: str, to_lang: str) -> str:
        """Convert type from one language to another"""
        try:
            conversion_map = self.type_conversions["cross_language_mappings"]
            
            # Handle numeric types
            if type_str in conversion_map["numeric"].get(f"{from_lang}_to_{to_lang}", {}):
                return conversion_map["numeric"][f"{from_lang}_to_{to_lang}"][type_str]
            
            # Handle array types
            if type_str in conversion_map["arrays"].get(f"{from_lang}_to_{to_lang}", {}):
                return conversion_map["arrays"][f"{from_lang}_to_{to_lang}"][type_str]
            
            # If no conversion found, return original type
            logger.warning(f"No conversion found for {type_str} from {from_lang} to {to_lang}")
            return type_str
            
        except Exception as e:
            logger.error(f"Type conversion failed: {str(e)}")
            raise TypeConversionError(f"Failed to convert type {type_str}: {str(e)}")

    def convert_structure(self, structure: dict, from_lang: str, to_lang: str) -> dict:
        """Convert entire problem structure from one language to another"""
        try:
            converted_structure = structure.copy()
            
            # Convert input structure
            for input_field in converted_structure.get("input_structure", []):
                field_parts = input_field["Input Field"].split()
                if len(field_parts) >= 2:
                    field_parts[0] = self.convert_type(field_parts[0], from_lang, to_lang)
                    input_field["Input Field"] = " ".join(field_parts)
            
            # Convert output structure
            if "output_structure" in converted_structure:
                field_parts = converted_structure["output_structure"]["Output Field"].split()
                if len(field_parts) >= 2:
                    field_parts[0] = self.convert_type(field_parts[0], from_lang, to_lang)
                    converted_structure["output_structure"]["Output Field"] = " ".join(field_parts)
            
            return converted_structure
            
        except Exception as e:
            logger.error(f"Structure conversion failed: {str(e)}")
            raise TypeConversionError(f"Failed to convert structure: {str(e)}") 