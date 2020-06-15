import uuid

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from ..models import Recipe, Ingredient

from ..serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def create_recipe(ingredients_count=5):
    """
    Creates a dummy recipe for testing
    """
    payload = build_random_recipe_payload(ingredients_count)
    ingredients = payload['ingredients']
    del payload['ingredients']

    recipe = Recipe.objects.create_recipe(
        recipe_data=payload,
        ingredients=ingredients
    )

    return recipe


def build_random_recipe_payload(ingredients_count=5):
    payload = {'name': f'random recipe name {str(uuid.uuid4())}',
               'description': f'random recipe description {str(uuid.uuid4())}',
               'ingredients': []}
    for i in range(ingredients_count):
        payload['ingredients'].append(
            {'name': f'Random ingredient {str(uuid.uuid4())}'}
        )

    return payload


def are_equal(recipe_payload, recipe):
    for key in recipe_payload.keys():
        if key != 'ingredients':
            if recipe_payload[key] != getattr(recipe, key):
                return False
        else:
            if len(recipe_payload['ingredients']) != len(recipe.ingredients):
                return False

            for i in range(len(recipe_payload['ingredients'])):
                ingredient_payload = recipe_payload['ingredients'][i]['name']
                ingredient_stored = getattr(
                    recipe.ingredients.all()[i],
                    'name'
                )
                if ingredient_payload != ingredient_stored:
                    return False

        return True


def recipe_detail_url(recipe_id):
    """
    Return recipe_detail_url
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])


class PublicRecipeApiTest(TestCase):
    """
    Test recipes api methods
    """

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """
        Test retrieving all available recipes
        """
        create_recipe(3)
        create_recipe(6)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """
        Test creating a recipe successfully
        """
        payload = build_random_recipe_payload(5)

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        self.assertTrue(are_equal(payload, recipe))

    def test_full_update_recipe(self):
        """
        Test updating an existing successfully
        """
        recipe = create_recipe(5)

        payload = build_random_recipe_payload(9)
        detail_url = recipe_detail_url(recipe.id)
        res = self.client.put(detail_url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertTrue(are_equal(payload, recipe))
        self.assertEqual(len(Ingredient.objects.all()), 9)
        for ingredient in Ingredient.objects.all():
            self.assertEqual(ingredient.recipe, recipe)

    def test_partial_update_recipe(self):
        """
        Test partial update on an existing recipe
        """
        recipe = create_recipe(4)
        original_name = recipe.name

        payload = build_random_recipe_payload(6)
        del payload['name']

        detail_url = recipe_detail_url(recipe.id)
        res = self.client.patch(detail_url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, original_name)
        self.assertTrue(are_equal(payload, recipe))

        self.assertEqual(len(Ingredient.objects.all()), 6)
        for ingredient in Ingredient.objects.all():
            self.assertEqual(ingredient.recipe, recipe)

    def test_delete_recipe(self):
        """
        Test delete recipe works successfully
        """
        recipe1 = create_recipe(8)
        recipe2 = create_recipe(3)

        detail_url = recipe_detail_url(recipe1.id)
        res = self.client.delete(detail_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.all().count(), 1)
        self.assertEqual(Recipe.objects.all()[0].id, recipe2.id)

        self.assertEqual(len(Ingredient.objects.all()), 3)
        for ingredient in Ingredient.objects.all():
            self.assertEqual(ingredient.recipe, recipe2)
