import os
import json
import random
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class PromptManager:
    def __init__(self):
        self.base_path = Path(__file__).parent / "prompts"
        self.concepts_path = self.base_path / "concepts"
        self.complexity_path = self.base_path / "complexity"
        self.contexts_path = self.base_path / "contexts"
        
        # Create directories if they don't exist
        self.concepts_path.mkdir(parents=True, exist_ok=True)
        self.complexity_path.mkdir(parents=True, exist_ok=True)
        self.contexts_path.mkdir(parents=True, exist_ok=True)

        # Track last used categories to avoid repetition
        self.last_used = {
            'category': None,
            'type': None
        }

    def _normalize_name(self, name: str) -> str:
        """Convert concept/complexity name to filename format"""
        logger.info(f"Normalizing name: {name}")
        normalized = name.lower().replace(" for ", "_").replace(" ", "_").replace("/", "_")
        logger.info(f"Normalized to: {normalized}")
        return normalized

    def _read_prompt_file(self, path: Path) -> Optional[str]:
        """Read prompt file if it exists"""
        try:
            if path.exists():
                return path.read_text().strip()
            return None
        except Exception as e:
            logger.warning(f"Failed to read prompt file {path}: {e}")
            return None

    def get_concept_prompt(self, concept: str) -> str:
        """Get concept-specific prompt with a randomly selected problem type"""
        try:
            # Set random seed at the start
            random.seed(os.urandom(8))
            
            concept_path = self._normalize_name(concept)
            config_path = self.concepts_path / concept_path / "config.json"
            
            with config_path.open() as f:
                config = json.load(f)
            
            # Get available categories excluding the last used one
            available_categories = [
                cat for cat in config["problem_types"] 
                if cat["category"] != self.last_used['category']
            ]
            
            if not available_categories:
                available_categories = config["problem_types"]
            
            # Select category and update last used
            category = random.choice(available_categories)
            logger.info(f"Selected category: {category['category']} (previous was: {self.last_used['category']})")
            self.last_used['category'] = category['category']
            
            # Get available problems excluding the last used type
            available_problems = [
                prob for prob in category["problems"]
                if prob["type"] != self.last_used['type']
            ]
            
            if not available_problems:
                available_problems = category["problems"]
            
            # Select problem and update last used
            problem = random.choice(available_problems)
            logger.info(f"Selected problem type: {problem['type']} (previous was: {self.last_used['type']})")
            self.last_used['type'] = problem['type']
            
            # Select variation
            variation = random.choice(problem["variations"])
            
            # Log the complete selection path
            logger.info(f"""
            Random Selection Path:
            Category: {category['category']} (from {len(available_categories)} available)
              └─ Problem Type: {problem['type']} (from {len(available_problems)} available)
                  └─ Variation: {variation} (from {len(problem['variations'])} available)
            """)
            
            # Load main prompt with fallback
            main_prompt = ""
            main_prompt_path = self.concepts_path / concept_path / "main_prompt.md"
            
            if main_prompt_path.exists():
                main_prompt = main_prompt_path.read_text().strip()
            else:
                logger.warning(f"Main prompt not found at: {main_prompt_path}")
                main_prompt = "Generate a programming problem suitable for beginners."
            
            return f"""
            {main_prompt}

            For this problem, use this specific type:
            Category: {category["category"]}
            Problem Type: {problem["type"]}
            Suggested Variation: {variation}

            Important: While using this problem type, create a unique variation that is
            substantially different from the suggested one. Do not reuse the exact suggested variation.
            Instead, create a new problem following the same pattern but with different requirements and context.
            """
            
        except Exception as e:
            logger.error(f"Error in get_concept_prompt: {str(e)}", exc_info=True)
            return "You are generating a programming problem for beginners. Focus on fundamental concepts and clear examples."

    def get_complexity_prompt(self, complexity: str) -> Optional[str]:
        """Get complexity-specific prompt"""
        filename = f"{self._normalize_name(complexity)}.md"
        return self._read_prompt_file(self.complexity_path / filename)

    def get_context_prompt(self, concept: str, complexity: str) -> Optional[str]:
        """Get context-specific prompt based on concept and complexity"""
        if "beginner" in concept.lower():
            return self._read_prompt_file(self.contexts_path / "beginner_contexts.md")
        elif complexity.lower() == "easy":
            return self._read_prompt_file(self.contexts_path / "beginner_contexts.md")
        elif complexity.lower() == "medium":
            return self._read_prompt_file(self.contexts_path / "intermediate_contexts.md")
        else:
            return self._read_prompt_file(self.contexts_path / "advanced_contexts.md")

    def get_problem_components(self, concept: str, complexity: str) -> Dict[str, Any]:
        # Normalize concept name for file paths
        concept_path = self._normalize_name(concept)
        
        # Load all components
        config = self._load_json(f"concepts/{concept_path}/config.json")
        main_prompt = self._read_file(f"concepts/{concept_path}/main_prompt.md")
        constraints = self._read_file(f"complexity/{complexity.lower()}/constraints.md")
        contexts = self._load_json("contexts/problem_contexts.json")
        
        # Randomly select problem type and context
        selected_type = self._select_random_problem(config["problem_types"])
        selected_context = self._select_random_context(contexts, concept_path, complexity.lower())
        
        return {
            "main_prompt": main_prompt,
            "constraints": constraints,
            "selected_type": selected_type,
            "selected_context": selected_context,
            "forbidden_types": config.get("forbidden_types", [])
        }
        
    def _select_random_problem(self, problem_types: list) -> dict:
        category = random.choice(problem_types)
        problem = random.choice(category["problems"])
        variation = random.choice(problem["variations"])
        return {
            "category": category["category"],
            "type": problem["type"],
            "variation": variation
        }

    def _load_json(self, filename: str) -> dict:
        path = self.base_path / filename
        if path.exists():
            return json.load(path.open())
        else:
            raise FileNotFoundError(f"File {path} does not exist")

    def _read_file(self, filename: str) -> str:
        path = self.base_path / filename
        if path.exists():
            return path.read_text().strip()
        else:
            raise FileNotFoundError(f"File {path} does not exist")

    def _select_random_context(self, contexts: dict, concept: str, complexity: str) -> str:
        # Implementation of _select_random_context method
        # This method should return a randomly selected context based on the given concept and complexity
        # You can implement this method based on your specific requirements
        # For now, we'll use a placeholder implementation
        return random.choice(contexts[concept][complexity]) 