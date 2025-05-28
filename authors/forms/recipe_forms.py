from django import forms
from recipes.models import Recipe

class AuthorRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', 'preparations_time_unit', 'servings_unit', 'servings_time_unit', 'preparation_steps', 'cover'

    