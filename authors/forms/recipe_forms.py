
from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict
from django.core.exceptions import ValidationError

from utils.string import is_positive_number

class AuthorRecipeForm(forms.ModelForm):
    def __ini__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class' , 'span-2')
        add_attr(self.fields.get('cover'), 'class' , 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', 'preparations_time_unit', 'servings_unit', 'servings_time_unit', 'preparation_steps', 'cover'
        widgets = {
            'cover' : forms.FileInput(
                attrs={
                    'class' :'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas','Pessoas'), 
                )
            ),
            'preparations_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            )
        }
    
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data= self.cleaned_data

        title =  cleaned_data.get('title')
        description = cleaned_data.get('description')

        if len(title) < 5:
            self.add_error['title'].append('Must have at least 5 characteres')
        
        if title == description:
            self.add_error['title'].append('Cannot be equal to description')
            self.add_error['description'].append('Cannot be equal to title')


        if self._errors:
            raise ValidationError(self._errors)

        return super_clean
    
    def clean_preparation_time(self):
        preparation_time =  self.cleaned_data.get('preparation_time')

        if not is_positive_number(preparation_time):
            self.add_error( 'preparation_time', 'Must be a positive number') 
        
        return preparation_time