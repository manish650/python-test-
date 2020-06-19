from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializers for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """serializer for Ingredient objects"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """serializer for Recipe objects"""
    ingredient = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tag = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredient', 'tag', 'time_minutes',
                  'price', 'link'
                  )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """serialized Recipe detail fields"""
    ingredient = IngredientSerializer(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """CLASS related to serialing image for recipe"""
    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
