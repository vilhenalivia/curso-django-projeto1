from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
import string
from random import SystemRandom

# Model Tag
class Tags(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    #Letras de A a Z com numeros e apenas 5 caracteres
                    string.ascii_letters + string.digits,
                    k=5
                )
            )
            self.slug - slugify(f'{self.name}-{rand_letters}')
        return super.save(args)