import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class JSONStorage:
    def __init__(self, storage_path: str = "data/recipes.json"):
        self.storage_path = storage_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Ensure the storage directory and file exist"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)

    def _read_recipes(self) -> List[Dict]:
        """Read all recipes from the JSON file"""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _write_recipes(self, recipes: List[Dict]):
        """Write recipes to the JSON file"""
        with open(self.storage_path, 'w') as f:
            json.dump(recipes, f, indent=2)

    def get_all_recipes(self) -> List[Dict]:
        """Get all recipes"""
        return self._read_recipes()

    def get_recipe_by_url(self, youtube_url: str) -> Optional[Dict]:
        """Get a recipe by YouTube URL"""
        recipes = self._read_recipes()
        for recipe in recipes:
            if recipe.get('youtube_url') == youtube_url:
                return recipe
        return None

    def add_recipe(self, recipe_data: Dict) -> Dict:
        """Add a new recipe"""
        recipes = self._read_recipes()
        
        # Add creation timestamp
        recipe_data['created_at'] = datetime.utcnow().isoformat()
        
        # Add ID (simple increment)
        recipe_data['id'] = len(recipes) + 1
        
        recipes.append(recipe_data)
        self._write_recipes(recipes)
        return recipe_data

    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete a recipe by ID"""
        recipes = self._read_recipes()
        for i, recipe in enumerate(recipes):
            if recipe.get('id') == recipe_id:
                recipes.pop(i)
                self._write_recipes(recipes)
                return True
        return False 