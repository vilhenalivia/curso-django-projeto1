from django.contrib import admin
from .models import Category, Recipe
from django.contrib.contenttypes.admin import GenericStackedInline
from tags.models import Tags
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
   list_display = [ 'id', 'title', 'created_at', 'is_published', 'author']
   list_display_links = ['title', 'created_at']
   search_fields = ['id', 'title', 'description', 'slug', 'preparation_steps']
   list_filter = ['category', 'author', 'is_published' ]
   list_per_page = 10
   list_editable = ['is_published']
   ordering = ['-id',]
   prepopulated_fields = {
      'slug' : ('title', )
   }
   autocomplete_fields = 'tags', 
