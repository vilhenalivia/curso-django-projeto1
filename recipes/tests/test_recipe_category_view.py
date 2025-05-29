from django.urls import resolve,reverse
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RescipeTestBase



class RecipeCategoryViewTest(RescipeTestBase):
    

    # CATEGORY
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response =self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

