from rest_framework import serializers

from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for ingredients
    """

    class Meta:
        model = Ingredient
        fields = ('name',)
        read_only_fields = ('id',)


def add_ingredients(recipe, ingredients):
    for ingredient in ingredients:
        Ingredient.objects.create(recipe=recipe, **ingredient)


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for recipes
    """
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'description', 'ingredients'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        recipe = Recipe(
            name=validated_data.get('name'),
            description=validated_data.get('description')
        )
        recipe.save()
        ingredients = validated_data.get('ingredients')
        add_ingredients(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):

        new_name = validated_data.get('name')
        if new_name:
            instance.name = new_name
        new_description = validated_data.get('description')
        if new_description:
            instance.description = new_description

        ingredients = validated_data.get('ingredients')
        if ingredients:
            ingredients_delete = Ingredient.objects.filter(recipe=instance)
            ingredients_delete.delete()
            add_ingredients(instance, ingredients)

        instance.save()

        return instance
