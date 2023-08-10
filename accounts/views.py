from django.http import HttpResponse
from django.shortcuts import render


def registerUser(request):
    return HttpResponse('this is a test reg form')
