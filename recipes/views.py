from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Recipe
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination
import os
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from tags.models import Tags
from django.utils import translation
from django.utils.translation import gettext as _
# Create your views here.

PER_PAGES =  int(os.environ.get('PER_PAGE' , 6))

class RecipeListViewBase(ListView):
    model = Recipe
    # Objeto
    context_object_name = 'recipes'
    # Ordena por padrão
    ordering = ['-id']
    # Nome do template
    template_name = 'recipes/pages/home.html'

    # Manipulação de query
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published= True)
        qs.select_related('author', 'category')
        qs.prefetch_related('tags', 'author__profile')
        return qs

    # Manipulação de contexto
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        #Paginação
        page_object , pagination_range = make_pagination(self.request, ctx.get('recipes'), PER_PAGES )
        html_language = translation.get_language()
        ctx.update ({ 
            'recipes' : page_object, 
            'pagination_range' : pagination_range,
            'html_language' : html_language,
        })
        return ctx

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    # Manipulação de contexto
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category_translation = _('Category')
        ctx.update ({
            'title': f'{ctx.get("recipes")[0].category.name} - {category_translation}'
        })
        return ctx
    
    # Manipulação de query
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(category__id= self.kwargs.get('category_id'))
        if not qs :
            raise Http404()
        return qs

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    # Manipulação de query
    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains = search_term)
            )
        )
        return qs
    
     # Manipulação de contexto
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('q', '')
        #Paginação
        page_object , pagination_range = make_pagination(self.request, ctx.get('recipes'), PER_PAGES )
        ctx.update ({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query' : f'&q={search_term}'
        })
        return ctx

class RecipeDetail(DetailView):


    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs =  super().get_queryset(*args, **kwargs)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'is_detail_page' : True
        })
        
        return ctx
    
class RecipeListViewHomeApi(RecipeListViewBase):

    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):

        recipes=  self.get_context_data()['recipes']
        recipes_dict = recipes.object_list.values()
        
        return JsonResponse(
            list(recipes_dict),
            safe=False
        )

class RecipeDetailApi(DetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri()[1:] + recipe_dict['cover'].url
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']

        return JsonResponse(
            recipe_dict,
            safe=False
        )
    
class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    # Manipulação de query
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug',  ''))
        return qs
    
     # Manipulação de contexto
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = Tags.object.filter(tags__slug=self.kwargs.get('slug',  '')).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag '

        ctx.update ({
            'page_title': f'{page_title}|',
        })
        return ctx