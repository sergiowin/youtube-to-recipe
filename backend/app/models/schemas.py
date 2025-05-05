from app import ma
from app.models.recipe import Recipe
from marshmallow import fields

class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    title = ma.auto_field()
    youtube_url = ma.auto_field()
    ingredients = fields.List(fields.String())
    instructions = fields.List(fields.String())
    cooking_time = ma.auto_field()
    servings = ma.auto_field()
    created_at = ma.auto_field()

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True) 