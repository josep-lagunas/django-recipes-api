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


class Recipe(models.Model):
    """
    Recipe object representation
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name
