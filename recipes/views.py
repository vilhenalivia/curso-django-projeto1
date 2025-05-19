from django.shortcuts import render
from django.http import HttpResponse
from utils.recipes.factory import make_recipe
from .models import Recipe

# Create your views here.

def home(request):
    recipes = Recipe.objects.all().order_by('-id')
    ctx= {
        'recipes': recipes,
        #[make_recipe() for _ in range(10)],
    }
    return render(request, 'recipes/pages/home.html', ctx)

def category(request, category_id):
    recipes = Recipe.objects.filter(category__id= category_id).order_by('-id')
    ctx= {
        'recipes': recipes,
        #[make_recipe() for _ in range(10)],
    }   
    return render(request, 'recipes/pages/home.html', ctx)


def recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    return render(request, 'recipes/pages/recipe-view.html', context= {
        'recipe': recipe,
        'is_detail_page': True,
    })

