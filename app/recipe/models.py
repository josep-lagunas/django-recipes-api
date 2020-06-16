from django.db import models


class Ingredient(models.Model):
    """
    Ingredient used in a recipe
    """
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients'
    )

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def create_recipe(self, recipe_data: dict, ingredients: list):
        recipe = self.create(**recipe_data)
        recipe.add_ingredients(ingredients)

        return recipe


class Recipe(models.Model):
    """
    Recipe object representation
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    objects = RecipeManager()

    def add_ingredients(self, ingredients):
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=self, **ingredient)

    def delete_ingredients(self):
        ingredients_delete = Ingredient.objects.filter(recipe=self)
        ingredients_delete.delete()

    def __str__(self):
        return self.name
