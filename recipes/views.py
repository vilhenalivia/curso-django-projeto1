from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, Http404
from utils.recipes.factory import make_recipe
from .models import Recipe

# Create your views here.

def home(request):
    
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    ctx= {
        'recipes': recipes,
        #[make_recipe() for _ in range(10)],
    }
    return render(request, 'recipes/pages/home.html', ctx)

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id= category_id, is_published= True).order_by('-id'))

    ctx= {
        'recipes': recipes,
        'title': f'{recipes.first().category.name} - Category',
        #[make_recipe() for _ in range(10)],
    }   
    return render(request, 'recipes/pages/category.html', ctx)


def recipe(request, id):
    recipe = Recipe.objects.filter(id=id, is_published= True).order_by('-id').first()
    return render(request, 'recipes/pages/recipe-view.html', context= {
        'recipe': recipe,
        'is_detail_page': True,
    })

