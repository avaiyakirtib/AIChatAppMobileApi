import json
import os
from app.db.models import User

# Construct the path to prompts.json relative to this file's location
PROMPT_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'prompts.json')

def load_prompts() -> dict:
    """Loads the prompts from the JSON file."""
    try:
        with open(PROMPT_FILE_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # In a real application, you'd want more robust error logging here
        return {}

def build_prompt(template_name: str, user: User) -> str:
    """
    Builds a personalized prompt by replacing placeholders in a template
    with the user's data.

    Args:
        template_name: The name of the prompt template to use (e.g., "main_system_prompt").
        user: The authenticated user object from the database.

    Returns:
        The final, personalized prompt string.
    """
    prompts = load_prompts()
    template = prompts.get(template_name)

    if not template:
        return f"Error: Prompt template '{template_name}' not found."

    # Define the mapping from placeholders to user attributes
    # Use a default value for any data that might be None
    placeholder_map = {
        "{{user_full_name}}": user.full_name or "our valued user",
        "{{user_age}}": user.age or "an unknown age",
        "{{user_gender}}": user.gender or "an unknown gender",
        "{{user_theme_preference}}": user.theme_preference or "the default theme"
    }

    # Replace all placeholders in the template
    for placeholder, value in placeholder_map.items():
        template = template.replace(placeholder, str(value))
    
    return template
