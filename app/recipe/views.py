from rest_framework import viewsets

from core.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Manage recipes requests
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """
        Retrieves the recipes filtered by name string if applies
        """
        name_filter = self.request.query_params.get('name')
        queryset = self.queryset

        if name_filter:
            queryset = queryset.filter(name__istartswith=name_filter)

        return queryset.order_by('-id')
