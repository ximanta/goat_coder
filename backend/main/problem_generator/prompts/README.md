# Problem Generator Prompts

## Concept Structure
Each concept (like 'array', 'array_search') must have its own folder containing:
- `config.json`: Defines problem types and variations specific to that concept
  ```json
  {
    "problem_types": [
      {
        "category": "Category Name",
        "problems": [
          {
            "type": "Problem Type",
            "variations": ["variation1", "variation2", ...]
          }
        ]
      }
    ]
  }
  ```

## Required Files
- `/concepts/basic_programming/config.json`
- `/concepts/basic_programming/main_prompt.md`
- `/concepts/array/config.json`
- `/concepts/array_search/config.json`
- `/complexity/easy.md`

## How Prompts Are Used
1. `PromptManager` loads concept-specific configuration and main prompt
2. Combines with complexity constraints from the respective `.md` file
3. Adds context and avoid prompts
4. Final combined prompt is sent to LLM with function calling schema

## File Structure
```
prompts/
├── concepts/
│   ├── array/
│   │   └── config.json           (✓ Array-specific problems)
│   ├── array_search/
│   │   └── config.json           (✓ Array search problems)
│   └── basic_programming/
│       └── config.json           (✓ Basic programming problems)
├── complexity/
│   └── easy.md                   (✓ Complexity constraints)
└── contexts/
    └── beginner_contexts.md      (✓ Context suggestions)
```

## Context Selection
- For beginner concepts: uses `beginner_contexts.md`
- For easy complexity: uses `beginner_contexts.md`
- For medium/advanced: currently falls back to no context
