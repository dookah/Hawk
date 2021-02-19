from django.db.models import query
from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from urllib.parse import urlencode
from django.core import serializers
from rbacapp.models import Integration
import requests
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

@login_required
def meraki(request):
    #Retrieve the user ID from the authenticated auth0 session
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    user_id = auth0user.uid;

    query_set = Integration.objects.filter(user=user_id).all()
    meraki_set = query_set.filter(product='meraki').all()

    print(meraki_set.values())


    host = 'https://api.meraki.com/api/v0/organizations'

    headers = {
        'X-Cisco-Meraki-API-Key' : 'cf1b763bbed2799ba2deba56fc57c574347494e7'
    }
    
    request = requests.get(host, headers=headers)
    org_id = request.json()[0]['id']

    path = '/' + org_id + '/admins'
    request = requests.get(host + path, headers=headers)
    print(request.json())

    return HttpResponse("Hello, world. You're at the meraki index.")
    