from flask import jsonify, request
from app.api import bp
from app.models.recipe import Recipe
from app.models.schemas import recipe_schema, recipes_schema
from app.services.youtube import YouTubeService
from app.services.recipe_extractor import RecipeExtractor
from app import db
import os

youtube_service = YouTubeService()
recipe_extractor = RecipeExtractor()

@bp.route('/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes"""
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return jsonify(recipes_schema.dump(recipes))

@bp.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    """Get a specific recipe"""
    recipe = Recipe.query.get_or_404(id)
    return jsonify(recipe_schema.dump(recipe))

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
    existing_recipe = Recipe.query.filter_by(youtube_url=url).first()
    if existing_recipe:
        return jsonify({'error': 'Recipe already exists', 
                       'recipe': recipe_schema.dump(existing_recipe)}), 409

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
        recipe = Recipe(
            title=recipe_info.get('title', 'Untitled Recipe'),
            youtube_url=url,
            ingredients=recipe_info.get('ingredients', []),
            instructions=recipe_info.get('instructions', []),
            cooking_time=recipe_info.get('cooking_time'),
            servings=recipe_info.get('servings')
        )
        
        # Save to database
        db.session.add(recipe)
        db.session.commit()

        return jsonify(recipe_schema.dump(recipe)), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to save recipe: {str(e)}'}), 500

@bp.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    """Delete a recipe"""
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return '', 204 