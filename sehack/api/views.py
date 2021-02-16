from django.db.models import query
from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from urllib.parse import urlencode
from django.core import serializers
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")
    