from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Recipe
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination_range

# Create your views here.

def home(request):
    
    recipes = Recipe.objects.filter(is_published=True)
    
    try: 
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
        
    paginator = Paginator(recipes, 4)
    page_object = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    ctx= {
        'recipes': page_object,
        'pagination_range' : pagination_range
        #[make_recipe() for _ in range(10)],
    }

    return render(request, 'recipes/pages/home.html', ctx)

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id= category_id, is_published= True).order_by('-id'))

    ctx= {
        'recipes': recipes,
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
        'recipes' : recipes,
    }


    return render(request, 'recipes/pages/search.html', ctx)
