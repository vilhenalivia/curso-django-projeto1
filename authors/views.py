from django.contrib import messages
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.urls import reverse

# Create your views here.
def register_view(request):

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    ctx ={
        'form': form,
        'form_action' : reverse('authors:create')
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