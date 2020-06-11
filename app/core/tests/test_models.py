from django.test import TestCase

from core.models import Ingredient, Recipe


class ModelsTests(TestCase):

    def test_ingredient_created_successfully(self):
        """
        Test the ingredient has been correctly created
        """
        recipe = Recipe.objects.create(
            name='Spaghetti al pesto',
            description='Spaghetti al pesto'
        )
        ingredient = Ingredient.objects.create(
            name='Cucumber', recipe=recipe
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_created_successfullly(self):
        """
        Test the recipe has been correctly created
        """
        description = 'Italian pasta dish from Rome made' \
                      'with egg, hard cheese, cured pork,' \
                      'and black pepper'
        recipe = Recipe.objects.create(
            name='Spaghetti carbonara',
            description=description
        )

        self.assertEqual(str(recipe), recipe.name)
        self.assertEqual(recipe.description, description)
