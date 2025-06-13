from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import *




class RegisterForm(forms.ModelForm):
    #PlaceHolders
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: Jonh')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')
        

    # Reescrita 
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators= [strong_password],
        label= 'Password'
    )


    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput()
        
    )

    username = forms.CharField(
        required=True,
        help_text= 'Username must have letters, numbers or one of those @.+-_.The length should be between 4 and 150 characters.',
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length' : 'Username must have less than 150 characters'
        },
        label = 'Username',
        min_length= 4,
        max_length= 150
    )

    # METADADOSs
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
            'email': 'The e-mail must be valid.'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email','')
        exists = User.objects.filter(email = email).exists()

        if exists:
            raise ValidationError('User e-mail is already in use', code='invalid')
        
        return email

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