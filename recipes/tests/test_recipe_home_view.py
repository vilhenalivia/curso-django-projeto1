from django.urls import resolve,reverse
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RescipeTestBase
from unittest.mock import patch


class RecipeHomeViewTest(RescipeTestBase):
    
    # HOME
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response =self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response =self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        Recipe.objects.get(pk=1).delete()
        response =self.client.get(reverse("recipes:home"))
        self.assertIn('<h1>No recipes found here</h1>',response.content.decode('utf-8'))

    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGES', new=4):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 4)
            self.assertEqual(len(paginator.get_page(2)), 4)
            self.assertEqual(len(paginator.get_page(3)), 1)
