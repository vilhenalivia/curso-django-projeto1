from django.test import TestCase
from django.urls import reverse 

# Teste de Url
class RecipeURLsTest(TestCase):
    # HOME
    def test_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')

    # CATEGORY
    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')
    
    # DETAIL
    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'pk': 1})
        self.assertEqual(url, '/recipes/1/')

    # SEARCH
    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')

# RED - GREEN - REFACTOR 