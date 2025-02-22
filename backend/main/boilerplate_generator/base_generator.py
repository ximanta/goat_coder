from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple

class BaseBoilerplateGenerator(ABC):
    @abstractmethod
    def convert_type(self, type_str: str) -> str:
        """Convert generic type to language-specific type."""
        pass

    @abstractmethod
    def parse_input_field(self, input_field: str) -> Tuple[str, str]:
        """Parse input field string to get type and name."""
        pass

    @abstractmethod
    def generate_boilerplate(self, structure: Dict) -> str:
        """Generate language-specific boilerplate code."""
        pass

    @abstractmethod
    def generate_test_case(self, test_case: Dict, function_name: str) -> str:
        """Generate language-specific test case."""
        pass

    @abstractmethod
    def get_imports(self) -> List[str]:
        """Get required imports for the language."""
        pass
