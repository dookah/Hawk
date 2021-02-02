from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    ctx = {
        'name' : 'Josh'
    }

    return render(request, 'rbacapp/index.html', ctx)
    
# Create your views here.
