from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from django.utils.decorators import method_decorator

def index(request):
    context = {}
    return render(request, 'dashboard.html', context)
