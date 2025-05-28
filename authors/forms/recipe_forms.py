from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr

class AuthorRecipeForm(forms.ModelForm):
    def __ini__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                    ('Pedaços', 'Pedaçoes'),
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
    