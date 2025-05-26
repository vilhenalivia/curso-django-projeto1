from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Recipe
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination
import os
from django.contrib import messages
# Create your views here.

PER_PAGES =  int(os.environ.get('PER_PAGE' , 6))

def home(request):
    
    # Query
    recipes = Recipe.objects.filter(is_published=True)
    
    # Pagination
    page_object , pagination_range = make_pagination(request, recipes, PER_PAGES )
    
    # context
    ctx= {
        'recipes': page_object,
        'pagination_range' : pagination_range
    }

    return render(request, 'recipes/pages/home.html', ctx)

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id= category_id, is_published= True).order_by('-id'))

    page_object , pagination_range = make_pagination(request, recipes, PER_PAGES )
    

    ctx= {
        'recipes': page_object,
        'pagination_range' : pagination_range,
        'title': f'{recipes[0].category.name} - Category',
        #[make_recipe() for _ in range(10)],
    }   
    return render(request, 'recipes/pages/category.html', ctx)

def recipe(request, id):
    recipe = get_object_or_404(Recipe.objects.filter(pk=id, is_published= True)) 
    return render(request, 'recipes/pages/recipe-view.html', context= {
        'recipe': recipe,
        'is_detail_page': True,
    })

def search(request):
    search_term = request.GET.get('q',' ').strip()

    if not search_term:
        raise Http404()
    
    page_object , pagination_range = make_pagination(request, recipes, PER_PAGES )
    
    recipes =  Recipe.objects.filter(
        Q (
            Q(title__icontains = search_term ) |
            Q(description__icontains = search_term)
        ),
        is_published = True
    ).order_by('-id')
    
    
    ctx={
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes' : page_object,
        'pagination_range' : pagination_range,
        'additional_url_query' : f'&q={search_term}'
    }


    return render(request, 'recipes/pages/search.html', ctx)
