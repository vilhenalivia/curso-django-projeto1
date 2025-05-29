from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from authors.forms.recipe_forms import AuthorRecipeForm
from recipes.models import Recipe

class DashboardRecipe():

    # Pega a receita
    def get_recipe(self, id):
        recipe = None

        # Se receber um id
        if id: 
            recipe = Recipe.objects.filter(
                is_published = False,
                author= self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404()
            
        return recipe

    # Rendereriza a página
    def render_recipe(self, form):
        ctx  ={
            'form' : form
        }

        return render(self.request, 'authors/pages/dashboard_recipe.html', ctx)

    # GET
    def get(self, *args, **kwargs):
        # Pega uma recipe
        recipe = self.get_recipe(kwargs.get(id))
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)     
    
    # POST
    def post(self, request, id):
        # Pega uma recipe
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(data=request.POST or None, files=request.FILES or None ,instance=recipe)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.is_published = False
            recipe.save()
            messages.success(request, "Sua receita foi salva com sucesso!")
            return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

        return self.render_recipe(form)