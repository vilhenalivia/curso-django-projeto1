from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from authors.forms.recipe_forms import AuthorRecipeForm
from recipes.models import Recipe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(View):
    # Pega a receita
    def get_recipe(self, id=None):
        recipe = None

        # Se receber um id
        if id is not None: 
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
    def get(self, request, id=None):
        # Pega uma recipe
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)     
    
    # POST
    def post(self, request, id=None):
        # Pega uma recipe
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(data=request.POST or None, files=request.FILES or None ,instance=recipe)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.is_published = False
            recipe.save()
            messages.success(request, "Sua receita foi salva com sucesso!")
            return redirect(reverse('authors:dashboard_recipe_edit', args=( recipe.id, )))

        return self.render_recipe(form)