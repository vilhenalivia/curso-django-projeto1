from django.db import models
from django.contrib.auth.models import User 
from django.urls import reverse
from django.utils.text import slugify
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
    
    # Ver no site
    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id))
    
    # slug como titulo da receita 
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            # Garante unicidade
            while Recipe.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug

        return super().save(*args, **kwargs)