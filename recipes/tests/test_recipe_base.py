from django.test import TestCase
from recipes.models import Category, Recipe
from django.contrib.auth.models import User


class RescipeTestBase(TestCase):
    def setUp(self):
        self.make_recipe()
        return super().setUp()

    def make_category(self, name ='Category' ):
        return Category.objects.create(name=name)
    
    # def make_author(
    #     self,
    #     first_name='user',
    #     last_name= 'name',
    #     username= 'username',
    #     password= '123456',
    #     email='username@emai.com'     
    # ):
    #     return User.objects.create_user(
    #         first_name=first_name,
    #         last_name= last_name,
    #         username= username,
    #         password= password,
    #         email=email
    #     )
    def make_author(self, **kwargs):
        import uuid
        unique_username = kwargs.get('username', f"username_{uuid.uuid4().hex}")
        return User.objects.create_user(
            first_name=kwargs.get('first_name', 'user'),
            last_name=kwargs.get('last_name', 'name'),
            username=unique_username,
            password=kwargs.get('password', '123456'),
            email=kwargs.get('email', f"{unique_username}@email.com"),
        )
    
    def make_recipe(
        self,
        category_data= None,
        author_data= None,
        title = 'Recipe Title',
        description = 'Recipe Desciption',
        slug = 'recipe-slug',
        preparation_time = 10,
        preparations_time_unit = 'Minutos',
        servings_time_unit = 5,
        servings_unit = 'Porções',
        preparation_steps = 'Recipe Preparation Steps',
        preparation_steps_is_html = False,
        is_published = True,           
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data ={}
        return Recipe.objects.create(
            category= self.make_category(**category_data),
            author= self.make_author(**author_data),
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparations_time_unit = preparations_time_unit,
            servings_time_unit = servings_time_unit,
            servings_unit = servings_unit,
            preparation_steps = preparation_steps,
            preparation_steps_is_html = preparation_steps_is_html,
            is_published = is_published,
        )