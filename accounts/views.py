from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserForm

def registerUser(request):
    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)
