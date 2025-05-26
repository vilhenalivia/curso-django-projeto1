from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    # Checagem se o que vem a frente está entre A a Z minusculo e minusculo e entre 0 e 9
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )



class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['first_name'], 'Ex.: Jonh')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators= [strong_password]
    )


    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })

    )

    # METADADOS
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels ={
            'first_name': 'Fist Name',
            'last_name': 'Last Name',
            'username' : 'Username',
            'email': 'E-mail', 
            'password' : 'Password',
        }
        
        help_texts = {
            'email': 'Digite um email válido'
        }

    def clean(self):
        cleaned_data = self.cleaned_data  # ← sem parênteses!
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError({ 
                'password': 'Password and Password2 must be equal', 
                'password2': 'Password and Password2 must be equal'
            })

        return cleaned_data