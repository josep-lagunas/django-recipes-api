from django.test import TestCase

from ..models import Ingredient, Recipe
from .test_recipe_api import build_random_recipe_payload, are_equal


class ModelsTests(TestCase):
    def test_ingredient_created_successfully(self):
        """
        Test the ingredient has been correctly created
        """
        payload = build_random_recipe_payload(1)
        ingredients = payload['ingredients']

        del payload['ingredients']

        Recipe.objects.create_recipe(recipe_data=payload,
                                     ingredients=ingredients)
        ingredients_saved = Ingredient.objects.all()

        self.assertEqual(len(ingredients_saved), 1)
        self.assertEqual(str(ingredients_saved[0]), ingredients[0]['name'])

    def test_recipe_created_successfully(self):
        """
        Test the recipe has been correctly created
        """
        payload = build_random_recipe_payload(8)

        ingredients = payload['ingredients']
        del payload['ingredients']

        recipe = Recipe.objects.create_recipe(recipe_data=payload,
                                              ingredients=ingredients)

        self.assertTrue(are_equal(payload, recipe))
