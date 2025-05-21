from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
# Cada modulo representa uma tabela no Banco de dados
class Category(models.Model):
    name = models.CharField(max_length=65)
    def __str__(self):
        return self.name

class Recipe(models.Model):
    # Colunas -> Atributos
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparations_time_unit = models.CharField(max_length=65)
    servings_time_unit = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    # Data criada autoáticamente na hora que for usado
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    # Relação 
    # -> Se apagar a categoria fica o campo nulo
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
