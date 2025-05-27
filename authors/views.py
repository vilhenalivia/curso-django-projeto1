from django.contrib import messages
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from .forms import RegisterForm, LoginForm
from django.urls import reverse

# Create your views here.
def register_view(request):

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    ctx ={
        'form': form,
        'form_action' : reverse('authors:register_create')
    }
    
    return render(request, "authors/pages/register_view.html", ctx)

def register_create(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    request.session['register_form_data'] =  POST
    form = RegisterForm(POST)
    
    if form.is_valid():
        user = form.save(commit=False) 
        user.set_password(user.password)
        user.save()
        request.session.pop('register_form_data', None)
        messages.success(request, 'Your user is created, please log in.')
        

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    ctx ={
        'form' :  form,
        'form_action' : reverse('authors:login')
    }
    return render(request, 'authors/pages/login.html', ctx)

def login_create(request):
    return render(request, 'authors/pages/login.html')
    