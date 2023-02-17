from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def manipulateImage(request):
    template = loader.get_template('game.html')
    return HttpResponse(template.render())
