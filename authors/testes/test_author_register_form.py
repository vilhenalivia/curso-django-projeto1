from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized

class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail' ),
        ('first_name', 'Ex.: Jonh'),
        ('last_name', 'Ex.: Doe' ),
        ('password','Type your password'),
        ('password2', 'Repeat your password')
    ])
    def test_field_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)
    

    @parameterized.expand([
        ('username', 'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.'),
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        ('email', 'The e-mail must be valid.'),
    ])
    def test_field_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)
        
    @parameterized.expand([
        ('first_name', 'Fist Name'),
        ('last_name', 'Last Name'),
        ('username' , 'Username'),
        ('email', 'E-mail'),
        ('password' , 'Password'),
    ])
    def test_field_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)