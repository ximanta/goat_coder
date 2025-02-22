from enum import Enum
from typing import Type
from .base_generator import BaseBoilerplateGenerator
from .java_boilerplate_generator import JavaBoilerplateGenerator
from .python_boilerplate_generator import PythonBoilerplateGenerator

class Language(Enum):
    JAVA = "java"
    PYTHON = "python"

class BoilerplateGeneratorFactory:
    _generators = {
        Language.JAVA: JavaBoilerplateGenerator,
        Language.PYTHON: PythonBoilerplateGenerator
    }

    @classmethod
    def get_generator(cls, language: Language) -> BaseBoilerplateGenerator:
        generator_class = cls._generators.get(language)
        if not generator_class:
            raise ValueError(f"Unsupported language: {language}")
        return generator_class()

    @classmethod
    def register_generator(cls, language: Language, generator_class: Type[BaseBoilerplateGenerator]):
        """Register a new language generator"""
        cls._generators[language] = generator_class
