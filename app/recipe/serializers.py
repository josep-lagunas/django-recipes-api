from rest_framework import serializers

from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for ingredients
    """

    class Meta:
        model = Ingredient
        fields = ('name',)
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for recipes
    """
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.get('ingredients')
        del validated_data['ingredients']
        recipe = Recipe.objects.create_recipe(recipe_data=validated_data,
                                              ingredients=ingredients)

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
            instance.delete_ingredients()
            instance.add_ingredients(ingredients)

        instance.save()

        return instance
