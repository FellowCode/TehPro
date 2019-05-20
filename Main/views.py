from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'Main/Index.html')

def debug(request):
    from TehPro.settings import DEBUG
    return HttpResponse(DEBUG)
