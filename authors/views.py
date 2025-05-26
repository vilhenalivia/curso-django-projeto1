from django.http import Http404
from django.shortcuts import redirect, render
from .forms import RegisterForm

# Create your views here.
def register_view(request):

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm()

    # context
    ctx ={
        'form' : form,
    }
    
    return render(request, "authors/pages/register_view.html", ctx)

def register_create(request):

    if not request.POST:
        raise Http404()
    
    POST = request.POST
    request.session['register_form_data'] =  POST
    form = RegisterForm(POST)
    
    return redirect('authors:register')