from flask import jsonify, request
from app.api import bp
from app.services.youtube import YouTubeService
from app.services.recipe_extractor import RecipeExtractor
from app.services.storage import JSONStorage

youtube_service = YouTubeService()
recipe_extractor = RecipeExtractor()
storage = JSONStorage()

@bp.route('/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes"""
    recipes = storage.get_all_recipes()
    return jsonify(recipes)

@bp.route('/recipes/process', methods=['POST'])
def process_recipe():
    """Process a YouTube video URL to extract recipe"""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url = data['url']
    
    # Validate URL
    if not youtube_service.validate_url(url):
        return jsonify({'error': 'Invalid YouTube video URL'}), 400

    # Check if recipe already exists
    existing_recipe = storage.get_recipe_by_url(url)
    if existing_recipe:
        return jsonify({'error': 'Recipe already exists', 
                       'recipe': existing_recipe}), 409

    # Fetch transcript
    try:
        transcript = youtube_service.fetch_transcript(url)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Process transcript and extract recipe
    recipe_info = recipe_extractor.extract_recipe(transcript)
    if not recipe_info:
        return jsonify({'error': 'Failed to extract recipe information'}), 400

    try:
        # Create new recipe
        recipe = {
            'title': recipe_info.get('title', 'Untitled Recipe'),
            'youtube_url': url,
            'ingredients': recipe_info.get('ingredients', []),
            'instructions': recipe_info.get('instructions', []),
            'cooking_time': recipe_info.get('cooking_time'),
            'servings': recipe_info.get('servings')
        }
        
        # Save to storage
        saved_recipe = storage.add_recipe(recipe)
        return jsonify(saved_recipe), 201

    except Exception as e:
        return jsonify({'error': f'Failed to save recipe: {str(e)}'}), 500

@bp.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """Delete a recipe by ID"""
    if storage.delete_recipe(recipe_id):
        return '', 204
    return jsonify({'error': 'Recipe not found'}), 404 